"""Chrome cookie clearing tool definition."""

import os
from tools.tools import Tool, ToolParameter


def get_tool(script_dir: str) -> Tool:
    """Get the Chrome cookie clearing tool definition."""
    return Tool(
        name="clear_chrome_cookies",
        description="Clear Chrome cookies for a specific domain to fix SSO (Single Sign-On) login loops. Common for corporate authentication issues where users get stuck in redirect loops with Microsoft, Okta, or Google SSO",
        category="authentication",
        script_path=os.path.join(script_dir, "clear_chrome_cookies.sh"),
        parameters=[
            ToolParameter(
                name="domain",
                type="string",
                description="The domain to clear cookies for (e.g., 'login.microsoftonline.com', 'accounts.google.com', 'okta.com')",
                required=True
            )
        ],
        requires_admin=False,
        risk_level="medium"
    )


