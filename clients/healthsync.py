"""HealthSync client configuration - LIMITED access (camera/mic only)."""

from clients.base_client import ClientConfig


def get_config() -> ClientConfig:
    """Get HealthSync client configuration."""
    return ClientConfig(
        client_name="HealthSync",
        client_id="health_001",
        allowed_tools=[
            "enable_camera_mic"  # ONLY camera/mic, no cookie clearing or Outlook reset
        ],
        agent_name="TechSupport Bot",
        agent_role="Level 1 Support Agent",
        custom_instructions="""
HealthSync is a healthcare company with strict security policies.

You can ONLY help with camera/microphone permissions for video conferencing.
For all other issues, escalate to Level 2 support.

Never modify browser settings or email profiles.
Always maintain HIPAA compliance in communications.
        """,
        tool_overrides={}
    )


