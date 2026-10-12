import pytest

from openhands.sdk.workspace import RemoteWorkspace
from openhands.workspace import APIRemoteWorkspace, OpenHandsCloudWorkspace


@pytest.mark.parametrize(
    "factory",
    [
        lambda: RemoteWorkspace(
            working_dir="/workspace",
            host="https://runtime.all-hands.dev",
            api_key="test",
        ),
        lambda: OpenHandsCloudWorkspace(
            cloud_api_url="https://app.all-hands.dev", cloud_api_key="test"
        ),
        lambda: APIRemoteWorkspace(
            runtime_api_url="https://runtime.all-hands.dev",
            runtime_api_key="test",
            server_image="test",
        ),
    ],
)
def test_hosted_provisioning_is_rejected_before_http(factory, monkeypatch):
    requests = []
    monkeypatch.setattr(
        "httpx.Client.request", lambda *args, **kwargs: requests.append(kwargs)
    )
    with pytest.raises(ValueError, match="OpenHands Cloud"):
        factory()
    assert requests == []
