"""Outlook profile reset tool definition."""

import os
from tools.tools import Tool, ToolParameter


def get_tool(script_dir: str) -> Tool:
    """Get the Outlook profile reset tool definition."""
    return Tool(
        name="reset_outlook_profile",
        description="Reset Microsoft Outlook profile to fix 'Loading Profile' or 'Stuck Syncing' issues. This creates a fresh Outlook profile while optionally backing up the old one",
        category="email",
        script_path=os.path.join(script_dir, "reset_outlook_profile.sh"),
        parameters=[
            ToolParameter(
                name="backup",
                type="string",
                description="Whether to backup the old profile before resetting (true or false)",
                required=False,
                enum=["true", "false"],
                default="true"
            )
        ],
        requires_admin=False,
        risk_level="high"
    )

