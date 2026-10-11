const {test} = require('node:test');
const assert = require('node:assert/strict');
const {classifyFiles, reusableEvidence, findValidatedMerge} = require('./ci-policy.cjs');

test('docs skip runtime; embedded prompts and unknown paths run every layer', () => {
  assert.equal(classifyFiles(['docs/setup.md', 'README.md']).python, false);
  assert.ok(Object.values(classifyFiles(['openhands-sdk/prompt.md'])).every(Boolean));
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
    actions: {listWorkflowRuns: async () => ({data: {workflow_runs: runs}})},
  }};
  const read = async (_, __, id) => ({version: 1, repository: 'Praxiss-Lab/praxis-sdk',
    run_id: id, event: 'pull_request', pull_number: 7, head_sha: 'head', tree: 'tree'});
  return {context, github, read};
}
const passed = {id: 12, status: 'completed', conclusion: 'success',
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
