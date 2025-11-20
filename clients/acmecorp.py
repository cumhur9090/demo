"""AcmeCorp client configuration - Full access to all tools."""

from clients.base_client import ClientConfig


def get_config() -> ClientConfig:
    """Get AcmeCorp client configuration."""
    return ClientConfig(
        client_name="AcmeCorp",
        client_id="acme_001",
        allowed_tools=[
            "enable_camera_mic",
            "clear_chrome_cookies",
            "reset_outlook_profile"
        ],
        agent_name="Joshua",
        agent_role="IT Support Specialist",
        custom_instructions="""
AcmeCorp uses Microsoft 365 and Zoom for collaboration.

Common issues:
- SSO with login.microsoftonline.com
- Zoom permissions on macOS
- Outlook sync problems

Always be professional and log all actions.
For high-risk operations, confirm with user first.
        """,
        tool_overrides={
            "clear_chrome_cookies": {
                "description": "Clear Chrome cookies for AcmeCorp SSO (login.microsoftonline.com)"
            }
        }
    )


