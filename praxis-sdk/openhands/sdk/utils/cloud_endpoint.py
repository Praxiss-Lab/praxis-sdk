from urllib.parse import urlsplit


def validate_self_hosted_endpoint(url: str | None) -> str | None:
    """Reject upstream hosted services before sending runtime credentials."""
    if url:
        hostname = (urlsplit(url).hostname or "").lower().rstrip(".")
        if any(
            hostname == domain or hostname.endswith(f".{domain}")
            for domain in ("all-hands.dev", "openhands.dev")
        ):
            raise ValueError(
                "OpenHands Cloud is not supported by Praxis. "
                "Configure a self-hosted endpoint or a direct model provider."
            )
    return url
