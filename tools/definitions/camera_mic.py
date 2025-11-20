"""Camera/Microphone permission tool definition."""

import os
from tools.tools import Tool, ToolParameter


def get_tool(script_dir: str) -> Tool:
    """Get the camera/mic tool definition."""
    return Tool(
        name="enable_camera_mic",
        description="Enable camera and microphone permissions for video conferencing apps like Zoom or Microsoft Teams when they cannot detect the camera or microphone",
        category="permissions",
        script_path=os.path.join(script_dir, "enable_camera_mic.sh"),
        parameters=[
            ToolParameter(
                name="app_name",
                type="string",
                description="The application name that needs camera/microphone access",
                required=True,
                enum=["Zoom", "Teams", "Microsoft Teams", "Slack", "Google Meet"]
            ),
            ToolParameter(
                name="permission_type",
                type="string",
                description="Type of permission to enable (camera, microphone, or both)",
                required=True,
                enum=["camera", "microphone", "both"],
                default="both"
            )
        ],
        requires_admin=False,
        risk_level="low"
    )


