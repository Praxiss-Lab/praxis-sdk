export function assertSelfHostedEndpoint(value: string): void {
  const hostname = new URL(value).hostname.toLowerCase().replace(/\.$/, '');
  if (
    ['all-hands.dev', 'openhands.dev'].some(
      (domain) => hostname === domain || hostname.endsWith(`.${domain}`)
    )
  ) {
    throw new Error('OpenHands Cloud is not supported. Configure a self-hosted endpoint.');
  }
}
