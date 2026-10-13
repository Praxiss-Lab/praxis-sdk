# Independent deployment

Praxis SDK runs with operator-managed Agent Servers and direct model providers.
No OpenHands hosted account or API key is required for these paths.

## Model transport

Configure a direct provider model and its credential, or an explicit self-hosted
proxy `base_url`. Legacy `openhands/` and `litellm_proxy/` model identifiers remain
readable but no longer select an upstream proxy automatically. Without an
explicit endpoint, proxy inference fails locally before forwarding credentials.
Legacy proxy snapshots retain their model identity; reconfigure the profile's
endpoint before resuming inference. This also applies to condenser models.
Metadata lookup must not send credentials to upstream hosted endpoints.

## Workspaces and critic

Use `LocalWorkspace`, `RemoteWorkspace` or `DockerWorkspace` for personal hosts
and containers. The legacy `OpenHandsCloudWorkspace` and `APIRemoteWorkspace`
APIs accept compatible operator-managed provisioning services only; they do not
provide a new App API service. Hosted upstream URLs are rejected before HTTP.
The optional critic defaults to loopback `http://127.0.0.1:8001`. Configure its
endpoint and service-issued credential explicitly; it is not a hosted benefit
bundled with a model-provider key. Saved critic configurations remain readable;
hosted endpoints are rejected when inference is requested.

## Repository automation

Cloud duplicate triage, upstream docs dispatch, upstream evaluation dispatch and
cross-repository/private-cloud version bumps are removed. Activity label cleanup
uses GitHub's API directly. Paid manual examples, integration and TODO jobs use
operator-configured model variables and credentials, with no upstream proxy URL
or SaaS credential default. The evaluation model resolver runs locally without
cloning and importing code from another repository.
Configure `LLM_BASE_URL` and `LLM_MODEL` repository variables for a self-hosted
proxy, and the applicable LLM secret before explicitly running paid jobs.
Routine PR validation does not need those credentials.

## Verification and limits

The isolation checks cover explicit HTTP, App API, device authorization,
WebSocket, model metadata, chat/Responses inference, critic and workspace paths.
Domains in the denial policy and historical migration fixtures are intentional;
licenses, original attribution and compatibility identifiers are retained.
This is application routing policy, not an operating-system egress firewall.
Arbitrary tools, MCP services and third-party gateways are operator-owned and
are not made safe by renaming the project. Docker/live LLM publication and
inference need separate environment-specific verification.
