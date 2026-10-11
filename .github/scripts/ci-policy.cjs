const {execFileSync} = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const SCOPES = ['python', 'typescript', 'server', 'examples', 'storage', 'security'];

function classifyFiles(files) {
  const scopes = Object.fromEntries(SCOPES.map(name => [name, false]));
  for (const file of files) {
    if (file.startsWith('docs/') || /^[^/]+\.(md|rst)$/i.test(file)) continue;
    if (file.startsWith('clients/typescript/')) {
      scopes.typescript = true;
      scopes.security = true;
    } else if (file.startsWith('examples/')) {
      scopes.python = true;
      scopes.examples = true;
    } else {
      // Unknown paths, shared Python packages, dependencies and CI affect all layers.
      for (const name of SCOPES) scopes[name] = true;
    }
  }
  return scopes;
}

function reusableEvidence(evidence, {repository, runId, pullNumber, headSha, tree,
  event = 'pull_request'}) {
  return evidence.version === 1 && evidence.repository === repository &&
    evidence.run_id === runId && evidence.event === event &&
    evidence.pull_number === pullNumber && evidence.head_sha === headSha &&
    evidence.tree === tree;
}

async function readEvidence(github, repo, runId) {
  const artifacts = await github.paginate(github.rest.actions.listWorkflowRunArtifacts,
    {...repo, run_id: runId, per_page: 100});
  const artifact = artifacts.find(item => item.name === 'sdk-ci-evidence' && !item.expired);
  if (!artifact || artifact.size_in_bytes > 100000) return null;
  const {data} = await github.rest.actions.downloadArtifact(
    {...repo, artifact_id: artifact.id, archive_format: 'zip'});
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'sdk-ci-evidence-'));
  try {
    const archive = path.join(directory, 'evidence.zip');
    fs.writeFileSync(archive, Buffer.from(data));
    return JSON.parse(execFileSync('unzip', ['-p', archive, 'evidence.json'],
      {encoding: 'utf8', maxBuffer: 100000}));
  } finally {
    fs.rmSync(directory, {recursive: true, force: true});
  }
}

async function findValidatedMerge(github, context, tree, read = readEvidence) {
  const {owner, repo} = context.repo;
  const params = {owner, repo};
  const {data: groups} = await github.rest.actions.listWorkflowRuns({
    ...params, workflow_id: 'sdk-validation.yml', event: 'merge_group',
    head_sha: context.sha, per_page: 100,
  });
  const latestGroup = groups.workflow_runs.filter(run => run.head_sha === context.sha)
    .sort((a, b) => b.id - a.id)[0];
  if (latestGroup) {
    if (latestGroup.status !== 'completed' || latestGroup.conclusion !== 'success') return '';
    const evidence = await read(github, params, latestGroup.id);
    return evidence && reusableEvidence(evidence, {
      repository: `${owner}/${repo}`, runId: latestGroup.id, pullNumber: 0,
      headSha: context.sha, tree, event: 'merge_group',
    }) ? latestGroup.html_url : '';
  }
  const {data: pulls} = await github.rest.repos.listPullRequestsAssociatedWithCommit(
    {...params, commit_sha: context.sha, per_page: 100});
  for (const pull of pulls) {
    if (!pull.merged_at || pull.merge_commit_sha !== context.sha ||
        pull.base.repo.full_name !== `${owner}/${repo}` ||
        pull.base.ref !== context.payload.repository.default_branch) continue;
    const {data} = await github.rest.actions.listWorkflowRuns({
      ...params, workflow_id: 'sdk-validation.yml', event: 'pull_request',
      head_sha: pull.head.sha, per_page: 100,
    });
    const latest = data.workflow_runs
      // GitHub can omit PR associations, especially after a PR is closed.
      // The run artifact below must still identify this exact PR and tree.
      .filter(run => run.head_sha === pull.head.sha &&
        (!run.pull_requests.length || run.pull_requests.some(pr => pr.number === pull.number)))
      .sort((a, b) => b.id - a.id)[0];
    // A failed, pending, cancelled or superseded latest run is never reusable.
    if (!latest || latest.status !== 'completed' || latest.conclusion !== 'success') continue;
    const evidence = await read(github, params, latest.id);
    if (evidence && reusableEvidence(evidence, {
      repository: `${owner}/${repo}`, runId: latest.id, pullNumber: pull.number,
      headSha: pull.head.sha, tree,
    })) return latest.html_url;
  }
  return '';
}

async function plan({github, context, core}) {
  const tree = execFileSync('git', ['rev-parse', 'HEAD^{tree}'], {encoding: 'utf8'}).trim();
  let reused = '';
  if (context.eventName === 'push') {
    try {
      reused = await findValidatedMerge(github, context, tree);
    } catch (error) {
      core.warning(`Cannot verify previous CI evidence; validating this push: ${error.message}`);
    }
  }
  let scopes = Object.fromEntries(SCOPES.map(name => [name, true]));
  const base = context.payload.pull_request?.base.sha ||
    context.payload.merge_group?.base_sha || context.payload.before;
  if (base && !/^0+$/.test(base) && context.eventName !== 'workflow_dispatch') {
    try {
      const files = execFileSync('git', ['diff', '--name-only', '--no-renames', base, 'HEAD'],
        {encoding: 'utf8', maxBuffer: 10000000}).trim().split('\n').filter(Boolean);
      scopes = classifyFiles(files);
    } catch (error) {
      core.warning(`Cannot determine changed files; running all checks: ${error.message}`);
    }
  }
  // Pushes without exact successful PR evidence run the entire suite.
  if (context.eventName === 'push' && !reused) {
    scopes = Object.fromEntries(SCOPES.map(name => [name, true]));
  }
  const evidence = {
    version: 1, repository: `${context.repo.owner}/${context.repo.repo}`,
    run_id: context.runId, event: context.eventName,
    pull_number: context.payload.pull_request?.number || 0,
    head_sha: context.payload.pull_request?.head.sha || context.sha, tree,
  };
  fs.writeFileSync(path.join(process.env.RUNNER_TEMP, 'evidence.json'), JSON.stringify(evidence));
  core.setOutput('validate', String(!reused));
  for (const [name, value] of Object.entries(scopes)) core.setOutput(name, String(value));
  await core.summary.addHeading('SDK validation policy')
    .addRaw(reused ? `Exact tested tree reused from ${reused}.` :
      `Validate ${tree}. Scopes: ${Object.entries(scopes).filter(([,v]) => v).map(([k]) => k).join(', ') || 'lint only'}.`)
    .write();
}

module.exports = {classifyFiles, reusableEvidence, findValidatedMerge, plan};
