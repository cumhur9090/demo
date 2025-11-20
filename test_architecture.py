"""
Quick test script to verify the scalable architecture works correctly.
"""

from clients import acmecorp, healthsync, faststart


def test_client_configs():
    """Test that all client configurations load correctly."""
    print("Testing Client Configurations...")
    print("=" * 60)
    
    clients = {
        "AcmeCorp": acmecorp.get_config(),
        "HealthSync": healthsync.get_config(),
        "FastStart": faststart.get_config()
    }
    
    for name, config in clients.items():
        print(f"\n{name}:")
        print(f"  Agent Name: {config.agent_name}")
        print(f"  Agent Role: {config.agent_role}")
        print(f"  Allowed Tools: {', '.join(config.allowed_tools)}")
        
        # Test tool registry
        registry = config.get_tool_registry()
        print(f"  Registered Tools: {len(registry.tools)}")
        
        # Verify only allowed tools are registered
        for tool_name in registry.tools.keys():
            assert tool_name in config.allowed_tools, f"Unauthorized tool {tool_name} in registry!"
        
        print(f"  ✅ Configuration valid")
    
    print("\n" + "=" * 60)
    print("✅ All client configurations passed!")


def test_tool_definitions():
    """Test that tool definitions are properly formatted."""
    print("\nTesting Tool Definitions...")
    print("=" * 60)
    
    config = acmecorp.get_config()
    registry = config.get_tool_registry()
    
    for tool_name, tool in registry.tools.items():
        print(f"\n{tool_name}:")
        print(f"  Category: {tool.category}")
        print(f"  Risk Level: {tool.risk_level}")
        print(f"  Parameters: {len(tool.parameters)}")
        print(f"  Requires Admin: {tool.requires_admin}")
        
        # Test OpenAI format conversion
        openai_format = tool.to_openai_format()
        assert "type" in openai_format
        assert "function" in openai_format
        assert "name" in openai_format["function"]
        print(f"  ✅ OpenAI format valid")
    
    print("\n" + "=" * 60)
    print("✅ All tool definitions passed!")


def test_permissions():
    """Test that permission system works correctly."""
    print("\nTesting Permission System...")
    print("=" * 60)
    
    # AcmeCorp should have all tools
    acme = acmecorp.get_config()
    acme_registry = acme.get_tool_registry()
    assert len(acme_registry.tools) == 3, "AcmeCorp should have 3 tools"
    print("✅ AcmeCorp: All 3 tools available")
    
    # HealthSync should only have camera_mic
    health = healthsync.get_config()
    health_registry = health.get_tool_registry()
    assert len(health_registry.tools) == 1, "HealthSync should have 1 tool"
    assert "enable_camera_mic" in health_registry.tools, "HealthSync should have camera_mic"
    assert "clear_chrome_cookies" not in health_registry.tools, "HealthSync should NOT have cookies"
    print("✅ HealthSync: Only camera_mic tool (restricted)")
    
    # FastStart should have 2 tools (no Outlook)
    fast = faststart.get_config()
    fast_registry = fast.get_tool_registry()
    assert len(fast_registry.tools) == 2, "FastStart should have 2 tools"
    assert "reset_outlook_profile" not in fast_registry.tools, "FastStart should NOT have Outlook"
    print("✅ FastStart: 2 tools, no Outlook (custom config)")
    
    print("\n" + "=" * 60)
    print("✅ Permission system working correctly!")


if __name__ == "__main__":
    try:
        test_client_configs()
        test_tool_definitions()
        test_permissions()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("\nThe scalable architecture is working correctly.")
        print("Run 'python main.py' to start the agent.")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

