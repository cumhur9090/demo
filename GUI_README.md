# IT Support Agent - GUI Version

Simple, clean chat interface for the IT Support Agent.

## 🎨 Features

**Minimal Design:**
- Clean chat interface
- Client selector dropdown
- Scrollable chat history
- Input field with send button
- Clear button to reset conversation

**Multi-Client Support:**
- Select from AcmeCorp, HealthSync, or FastStart
- Switch clients dynamically
- Each client has different available tools

**Real-Time Updates:**
- Tool execution shown in real-time
- Progress messages with 0.5s delays for demo visibility
- Color-coded messages (user, agent, tool output, errors)

## 🚀 How to Run

### Launch the GUI:

```bash
python gui.py
```

Or:

```bash
python3 gui.py
```

### Using the Interface:

1. **Select Client** - Choose from the dropdown at the top
2. **Type Message** - Enter your IT support request
3. **Send** - Click button or press Enter
4. **View Response** - Agent response appears with tool execution details
5. **Clear** - Reset conversation history

## 🎯 Example Interactions

### AcmeCorp (Full Access):
```
You: My Zoom camera isn't working
Joshua: I'll help you enable camera permissions...
[Tool executes: enable_camera_mic]
[System Settings opens, permission toggled]
Joshua: Done! Your camera should now work in Zoom.
```

### HealthSync (Limited Access):
```
You: I'm stuck in an SSO login loop
TechSupport Bot: I can only help with camera/microphone issues.
Please escalate to Level 2 support for SSO issues.
```

### FastStart (Custom Config):
```
You: Clear my Okta cookies
Alex: I'll clear the SSO cookies for you...
[Tool executes: clear_chrome_cookies]
[Chrome closes, cookies cleared, Chrome reopens]
Alex: Cookies cleared. Try logging in again.
```

## 🎬 Demo Features

**Visual Feedback:**
- All scripts have 0.5 second delays between steps
- Progress messages show each action
- Perfect for screen recording demos

**Status Indicators:**
- ✓ Connected as {Agent Name}
- ⏳ Processing...
- ✗ Error occurred

**Color Coding:**
- **Blue** - User messages
- **Green** - Agent responses  
- **Orange** - Tool execution details
- **Red** - Error messages

## 📐 UI Layout

```
┌─────────────────────────────────────────────────┐
│ Client: [Dropdown ▼]      ✓ Connected          │
├─────────────────────────────────────────────────┤
│                                                 │
│  You: My Zoom camera isn't working              │
│                                                 │
│  Joshua: I'll help you enable camera...         │
│                                                 │
│  🔧 Executing: enable_camera_mic                │
│     Arguments: {app: Zoom, type: both}          │
│                                                 │
│  [Tool output shown here...]                    │
│                                                 │
│  Joshua: Done! Your camera should work now.     │
│                                                 │
│                            [Scrollable]          │
├─────────────────────────────────────────────────┤
│ [Type your message here...    ] [Send] [Clear] │
└─────────────────────────────────────────────────┘
```

## 🔧 Technical Details

**Built with:**
- `tkinter` - Native Python GUI (no extra dependencies!)
- Threading - Non-blocking UI during tool execution
- ScrolledText - Smooth scrolling chat history

**GUI Features:**
- Responsive design
- Keyboard shortcuts (Enter to send)
- Auto-scroll to latest message
- Thread-safe UI updates

## 💡 Tips

1. **For best demo videos:**
   - Use full-screen mode
   - Tool execution shows clear progress (0.5s delays)
   - Each step is visible and readable

2. **Switching clients:**
   - Select different client from dropdown
   - Chat clears and new agent introduces itself
   - Only that client's tools are available

3. **Error handling:**
   - If OpenAI key is missing, error shown in red
   - Tool failures show clear error messages
   - Network errors handled gracefully

## 📊 Comparison: CLI vs GUI

| Feature | CLI | GUI |
|---------|-----|-----|
| Client Selection | At startup | Dropdown (switch anytime) |
| Chat History | Scrolls up | Scrollable window |
| Tool Output | Plain text | Color-coded |
| Demo-Friendly | Good | Excellent |
| Setup | Terminal | Double-click |

## 🎥 Perfect for Demos

This GUI is specifically designed for **recording demonstrations**:

✅ Clean, professional interface  
✅ Clear visual feedback  
✅ Tool execution progress visible  
✅ 0.5s delays for readability  
✅ No terminal clutter  
✅ Easy to follow on video  

---

**Ready to demo!** 🚀

Run `python gui.py` and start showcasing your IT Support Agent!

