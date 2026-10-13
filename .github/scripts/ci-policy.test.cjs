const {test} = require('node:test');
const assert = require('node:assert/strict');
const {execFileSync} = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {classifyFiles, reusableEvidence, findValidatedMerge} = require('./ci-policy.cjs');

test('docs skip runtime; embedded prompts and unknown paths run every layer', () => {
  assert.equal(classifyFiles(['docs/setup.md', 'README.md']).python, false);
  assert.ok(Object.values(classifyFiles(['praxis-sdk/prompt.md'])).every(Boolean));
  assert.ok(Object.values(classifyFiles(['new-component/config.json'])).every(Boolean));
  assert.ok(Object.values(classifyFiles(['uv.lock'])).every(Boolean));
});

test('TypeScript updates include integration and security without Python suites', () => {
  const scopes = classifyFiles(['clients/typescript/package-lock.json']);
  assert.equal(scopes.typescript, true);
  assert.equal(scopes.security, true);
  assert.equal(scopes.python, false);
});

test('an exact tree alone cannot reuse evidence from another PR, repository or run', () => {
  const expected = {repository: 'Praxiss-Lab/praxis-sdk', runId: 12,
    pullNumber: 7, headSha: 'head', tree: 'tree'};
  const valid = {version: 1, repository: expected.repository, run_id: 12,
    event: 'pull_request', pull_number: 7, head_sha: 'head', tree: 'tree'};
  assert.equal(reusableEvidence(valid, expected), true);
  for (const [key, value] of Object.entries({repository: 'other/repo', run_id: 11,
    pull_number: 8, head_sha: 'old', tree: 'different', event: 'push', version: 0})) {
    assert.equal(reusableEvidence({...valid, [key]: value}, expected), false);
  }
});

function fixture(runs, pullOverrides = {}) {
  const context = {repo: {owner: 'Praxiss-Lab', repo: 'praxis-sdk'}, sha: 'merge',
    payload: {repository: {default_branch: 'main'}}};
  const pull = {number: 7, merged_at: 'today', merge_commit_sha: 'merge',
    base: {repo: {full_name: 'Praxiss-Lab/praxis-sdk'}, ref: 'main'},
    head: {sha: 'head'}, ...pullOverrides};
  const github = {rest: {
    repos: {listPullRequestsAssociatedWithCommit: async () => ({data: [pull]})},
    actions: {listWorkflowRuns: async ({event}) =>
      ({data: {workflow_runs: event === 'merge_group' ? [] : runs}})},
  }};
  const read = async (_, __, id) => ({version: 1, repository: 'Praxiss-Lab/praxis-sdk',
    run_id: id, event: 'pull_request', pull_number: 7, head_sha: 'head', tree: 'tree'});
  return {context, github, read};
}
const passed = {id: 12, head_sha: 'head', status: 'completed', conclusion: 'success',
  pull_requests: [{number: 7}], html_url: 'https://github.com/run/12'};

test('a merge reuses the latest successful PR run only for its exact tested tree', async () => {
  const {context, github, read} = fixture([passed]);
  assert.equal(await findValidatedMerge(github, context, 'tree', read), passed.html_url);
  assert.equal(await findValidatedMerge(github, context, 'other-tree', read), '');
});

test('new failed, queued and cancelled attempts invalidate an earlier success', async () => {
  for (const [status, conclusion] of [['completed', 'failure'], ['queued', null],
    ['completed', 'cancelled']]) {
    const newer = {...passed, id: 13, status, conclusion};
    const {context, github, read} = fixture([passed, newer]);
    assert.equal(await findValidatedMerge(github, context, 'tree', read), '');
  }
});

test('direct pushes, unrelated commits and missing artifacts require validation', async () => {
  for (const override of [{merged_at: null}, {merge_commit_sha: 'another'}]) {
    const {context, github, read} = fixture([passed], override);
    assert.equal(await findValidatedMerge(github, context, 'tree', read), '');
  }
  const {context, github} = fixture([passed]);
  assert.equal(await findValidatedMerge(github, context, 'tree', async () => null), '');
});

test('GitHub runs without PR associations reuse only artifact-proven PR identity', async () => {
  const {context, github, read} = fixture([{...passed, pull_requests: []}]);
  assert.equal(await findValidatedMerge(github, context, 'tree', read), passed.html_url);
  assert.equal(await findValidatedMerge(github, context, 'tree', async (...args) =>
    ({...await read(...args), pull_number: 8})), '');
  assert.equal(await findValidatedMerge(github, context, 'tree', async (...args) =>
    ({...await read(...args), repository: 'another/repo'})), '');
});

test('an unassociated newer failed or cancelled run prevents stale reuse', async () => {
  for (const [status, conclusion] of [['completed', 'failure'], ['queued', null],
    ['in_progress', null], ['completed', 'cancelled']]) {
    const newer = {...passed, id: 13, pull_requests: [], status, conclusion};
    const {context, github, read} = fixture([passed, newer]);
    assert.equal(await findValidatedMerge(github, context, 'tree', read), '');
  }
});

test('different heads and explicitly unrelated PRs cannot supply merge evidence', async () => {
  for (const run of [{...passed, head_sha: 'old'},
    {...passed, pull_requests: [{number: 8}]}]) {
    const {context, github, read} = fixture([run]);
    assert.equal(await findValidatedMerge(github, context, 'tree', read), '');
  }
});

test('merge queue reuse requires the exact successful group commit and provenance', async () => {
  const {context, github} = fixture([]);
  const group = {...passed, head_sha: context.sha, pull_requests: []};
  github.rest.actions.listWorkflowRuns = async () => ({data: {workflow_runs: [group]}});
  const evidence = {version: 1, repository: 'Praxiss-Lab/praxis-sdk', run_id: group.id,
    event: 'merge_group', pull_number: 0, head_sha: context.sha, tree: 'tree'};
  assert.equal(await findValidatedMerge(github, context, 'tree', async () => evidence), group.html_url);
  assert.equal(await findValidatedMerge(github, context, 'another', async () => evidence), '');
  assert.equal(await findValidatedMerge(github, context, 'tree', async () =>
    ({...evidence, head_sha: 'different'})), '');
  for (const conclusion of ['failure', 'cancelled']) {
    github.rest.actions.listWorkflowRuns = async () =>
      ({data: {workflow_runs: [group, {...group, id: 13, conclusion}]}});
    assert.equal(await findValidatedMerge(github, context, 'tree', async () => evidence), '');
  }
});

test('real Git event planning selects scopes and falls back safely on direct pushes', () => {
  const cases = [
    ['pull_request', 'docs/change.md', []],
    ['pull_request', 'docs/examples/catalog.md', ['examples']],
    ['pull_request', 'clients/typescript/change.ts', ['typescript', 'security']],
    ['pull_request', 'examples/change.py', ['python', 'examples']],
    ['pull_request', 'uv.lock', ['python', 'typescript', 'server', 'examples', 'storage', 'security']],
    ['pull_request', '.github/workflows/change.yml', ['python', 'typescript', 'server', 'examples', 'storage', 'security']],
    ['merge_group', 'clients/typescript/change.ts', ['typescript', 'security']],
    ['workflow_dispatch', 'docs/change.md', ['python', 'typescript', 'server', 'examples', 'storage', 'security']],
    ['push', 'docs/change.md', ['python', 'typescript', 'server', 'examples', 'storage', 'security']],
  ];
  for (const [eventName, file, expected] of cases) {
    const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'sdk-ci-plan-test-'));
    try {
      const env = {...process.env, GIT_AUTHOR_NAME: 'CI test', GIT_AUTHOR_EMAIL: 'ci@example.test',
        GIT_COMMITTER_NAME: 'CI test', GIT_COMMITTER_EMAIL: 'ci@example.test', RUNNER_TEMP: directory};
      const git = (...args) => execFileSync('git', args, {cwd: directory, env, encoding: 'utf8'}).trim();
      git('init', '--quiet');
      fs.writeFileSync(path.join(directory, 'base.txt'), 'base');
      git('add', '.');
      git('commit', '--quiet', '-m', 'base');
      const base = git('rev-parse', 'HEAD');
      fs.mkdirSync(path.dirname(path.join(directory, file)), {recursive: true});
      fs.writeFileSync(path.join(directory, file), 'change');
      git('add', '.');
      git('commit', '--quiet', '-m', 'change');
      const sha = git('rev-parse', 'HEAD');
      const tree = git('rev-parse', 'HEAD^{tree}');
      const context = {eventName, repo: {owner: 'Praxiss-Lab', repo: 'praxis-sdk'}, sha,
        runId: 99, payload: {before: base, repository: {default_branch: 'main'}}};
      if (eventName === 'pull_request') context.payload.pull_request = {number: 7,
        base: {sha: base}, head: {sha}};
      if (eventName === 'merge_group') context.payload.merge_group = {base_sha: base};
      const script = `
        const {plan} = require(${JSON.stringify(path.join(__dirname, 'ci-policy.cjs'))});
        const outputs = {};
        const summary = {addHeading() {return this}, addRaw() {return this}, async write() {}};
        const core = {setOutput(k,v) {outputs[k] = v}, warning() {}, summary};
        const github = {rest: {actions: {async listWorkflowRuns() {
          return {data: {workflow_runs: []}};
        }}, repos: {async listPullRequestsAssociatedWithCommit() {
          return {data: []};
        }}}};
        plan({github, context: ${JSON.stringify(context)}, core})
          .then(() => console.log(JSON.stringify(outputs))).catch(e => {console.error(e); process.exit(1)});
      `;
      const outputs = JSON.parse(execFileSync(process.execPath, ['-e', script],
        {cwd: directory, env, encoding: 'utf8'}));
      assert.equal(outputs.validate, 'true');
      const selected = Object.keys(outputs).filter(k => k !== 'validate' && outputs[k] === 'true');
      assert.deepEqual(selected, expected, `${eventName}: ${file}`);
      const evidence = JSON.parse(fs.readFileSync(path.join(directory, 'evidence.json'), 'utf8'));
      assert.equal(evidence.tree, tree);
      assert.equal(evidence.head_sha, sha);
      assert.equal(evidence.event, eventName);
    } finally {
      fs.rmSync(directory, {recursive: true, force: true});
    }
  }
});
