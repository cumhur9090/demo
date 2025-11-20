# IT Support Agent - Scalable Architecture

This document explains the new scalable, multi-client architecture.

## 🏗️ Architecture Overview

```
demo/
├── main.py                      # CLI entry point with client selection
├── agent.py                     # Core ITAgent class
├── memory.py                    # Conversation memory manager
├── tools/
│   ├── tools.py                 # Tool, ToolParameter, ToolRegistry classes
│   └── definitions/             # Individual tool definitions
│       ├── camera_mic.py
│       ├── chrome_cookies.py
│       └── outlook_profile.py
├── clients/
│   ├── base_client.py           # ClientConfig base class
│   ├── acmecorp.py              # Full access client
│   ├── healthsync.py            # Limited access client
│   └── faststart.py             # Custom SSO client
└── scripts/                     # Shell scripts (unchanged)
    ├── enable_camera_mic.sh
    ├── clear_chrome_cookies.sh
    └── reset_outlook_profile.sh
```

## 🔑 Key Components

### 1. Tool System (`tools/`)

**Tool Class** - Represents a single IT support tool with:
- `name`: Unique identifier
- `description`: What the tool does
- `category`: permissions, authentication, email
- `script_path`: Path to shell script
- `parameters`: List of ToolParameter objects
- `requires_admin`: Boolean flag
- `risk_level`: low, medium, high

**ToolRegistry** - Manages available tools:
- `register(tool)`: Add a tool
- `get(name)`: Retrieve a tool
- `to_openai_format()`: Convert to OpenAI function calling format

**Tool Definitions** (`tools/definitions/`) - Separate files for each tool:
- `camera_mic.py`: Camera/microphone permissions
- `chrome_cookies.py`: SSO cookie clearing
- `outlook_profile.py`: Outlook profile reset

### 2. Client System (`clients/`)

**ClientConfig Class** - Defines client-specific configuration:
- `client_name`: Display name (e.g., "AcmeCorp")
- `client_id`: Unique ID
- `allowed_tools`: List of tool names this client can use
- `agent_name`: Name of the agent (e.g., "Joshua")
- `agent_role`: Role description
- `custom_instructions`: Client-specific prompt additions
- `tool_overrides`: Per-tool customizations

**Three Example Clients:**

1. **AcmeCorp** - Full access
   - All tools: camera_mic, chrome_cookies, outlook_profile
   - Uses Microsoft 365 + Zoom
   - Agent: "Joshua"

2. **HealthSync** - Limited access
   - Only: camera_mic
   - Healthcare company with strict security
   - Cannot modify browser/email settings
   - Agent: "TechSupport Bot"

3. **FastStart** - Custom configuration
   - Tools: camera_mic, chrome_cookies
   - Uses Google Workspace + Okta (not Microsoft)
   - Custom SSO domains
   - No Outlook (uses Gmail)
   - Agent: "Alex"

### 3. Agent System (`agent.py`)

**ITAgent Class** - Core agent with client-based access control:
- Initializes with `ClientConfig`
- Builds client-specific system prompt
- Only exposes allowed tools to OpenAI
- Permission checking before tool execution
- Maintains conversation memory
- Handles tool execution and responses

### 4. Memory System (`memory.py`)

**ConversationMemory** - Manages chat history:
- Stores messages as list of dicts (role, content)
- Methods: `add_user_message()`, `add_assistant_message()`, `get_history()`, `clear()`
- Compatible with OpenAI API format

## 🎯 How It Works

### Client Selection Flow

1. User runs `python main.py`
2. System shows available clients with their tools
3. User selects a client (1-3)
4. Agent initializes with that client's config
5. Only that client's allowed tools are available

### Tool Execution Flow

1. User sends message: "My Zoom camera isn't working"
2. Agent analyzes with OpenAI (only sees allowed tools)
3. Agent decides to call `enable_camera_mic` tool
4. **Permission check**: Is tool in `client.allowed_tools`?
5. If yes: Execute script with arguments
6. Return result to user

### Permission Enforcement

```python
# Example: HealthSync user tries to clear cookies
User (HealthSync): "I'm stuck in an SSO loop"
Agent checks: "clear_chrome_cookies" in healthsync.allowed_tools?
Result: False
Agent response: "I can only help with camera/microphone issues. 
                Please escalate to Level 2 support for SSO issues."
```

## 🚀 Adding New Clients

1. Create new file in `clients/`:

```python
# clients/newcorp.py
from clients.base_client import ClientConfig

def get_config() -> ClientConfig:
    return ClientConfig(
        client_name="NewCorp",
        client_id="new_001",
        allowed_tools=["enable_camera_mic"],  # Choose tools
        agent_name="Sarah",
        agent_role="IT Assistant",
        custom_instructions="NewCorp-specific instructions...",
        tool_overrides={}
    )
```

2. Register in `main.py`:

```python
from clients import newcorp

CLIENTS = {
    "newcorp": newcorp.get_config(),
    # ... other clients
}
```

## 🔧 Adding New Tools

1. Create shell script in `scripts/`:

```bash
#!/bin/bash
# scripts/new_tool.sh
# Your automation logic here
```

2. Create tool definition in `tools/definitions/`:

```python
# tools/definitions/new_tool.py
from tools.tools import Tool, ToolParameter

def get_tool(script_dir: str) -> Tool:
    return Tool(
        name="new_tool",
        description="What this tool does",
        category="your_category",
        script_path=os.path.join(script_dir, "new_tool.sh"),
        parameters=[
            ToolParameter(
                name="param1",
                type="string",
                description="Parameter description",
                required=True
            )
        ],
        requires_admin=False,
        risk_level="low"
    )
```

3. Register in `clients/base_client.py`:

```python
from tools.definitions import new_tool

all_tools = {
    "new_tool": new_tool.get_tool(script_dir),
    # ... other tools
}
```

4. Add to client's `allowed_tools` list.

## 🎨 Customizing Tools Per Client

Use `tool_overrides` to customize tool behavior:

```python
ClientConfig(
    # ...
    tool_overrides={
        "clear_chrome_cookies": {
            "description": "Custom description for this client",
            "risk_level": "high"  # Override risk level
        }
    }
)
```

## 📊 Benefits

1. **Scalability**: Add clients without modifying core code
2. **Security**: Fine-grained tool permissions per client
3. **Customization**: Client-specific prompts and tool behavior
4. **Maintainability**: Separation of concerns
5. **Auditability**: Know exactly what each client can do
6. **Testability**: Easy to test individual components

## 🧪 Testing

Test client configurations:

```bash
python3 -c "from clients import acmecorp; config = acmecorp.get_config(); print(config.allowed_tools)"
```

Test tool registry:

```bash
python3 -c "from clients import healthsync; registry = healthsync.get_config().get_tool_registry(); print(list(registry.tools.keys()))"
```

Run the agent:

```bash
python main.py
```

## 🔜 Future Enhancements

- Role-based access control (RBAC)
- Time-based tool access (business hours only)
- Approval workflows for high-risk tools
- Tool usage analytics per client
- Dynamic tool loading from database
- Multi-language support
- Web UI with client portal

