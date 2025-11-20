"""FastStart client configuration - Custom SSO domain."""

from clients.base_client import ClientConfig


def get_config() -> ClientConfig:
    """Get FastStart client configuration."""
    return ClientConfig(
        client_name="FastStart Inc",
        client_id="fast_001",
        allowed_tools=[
            "enable_camera_mic",
            "clear_chrome_cookies"
            # No Outlook reset - they use Gmail
        ],
        agent_name="Alex",
        agent_role="Tier 1 IT Support",
        custom_instructions="""
FastStart uses Google Workspace and Okta for SSO.

For SSO issues, clear cookies for:
- accounts.google.com
- faststart.okta.com

We use Google Meet, not Zoom.
FastStart does not use Outlook - we're on Gmail/Google Workspace.
        """,
        tool_overrides={
            "clear_chrome_cookies": {
                "description": "Clear Chrome cookies for FastStart Okta SSO (faststart.okta.com or accounts.google.com)"
            }
        }
    )


