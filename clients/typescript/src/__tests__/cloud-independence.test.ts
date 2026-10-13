import { afterEach, expect, it, vi } from 'vitest';
import { HttpClient } from '../client/http-client';
import { CloudClient } from '../client/cloud-client';
import { startDeviceFlow } from '../client/device-flow-client';

afterEach(() => vi.unstubAllGlobals());

it('rejects hosted HTTP, App API and authorization without sending credentials', async () => {
  const fetch = vi.fn();
  vi.stubGlobal('fetch', fetch);
  await expect(
    new HttpClient({ baseUrl: 'https://app.all-hands.dev', apiKey: 'test' }).get('/api/settings')
  ).rejects.toThrow(/OpenHands Cloud/);
  await expect(
    new CloudClient({ host: 'https://app.all-hands.dev', apiKey: 'test' }).getOrganizations()
  ).rejects.toThrow(/OpenHands Cloud/);
  await expect(startDeviceFlow('https://app.all-hands.dev')).rejects.toThrow(/OpenHands Cloud/);
  expect(fetch).not.toHaveBeenCalled();
});
