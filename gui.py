"""
Simple GUI for IT Support Agent - Minimal chat interface.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import os
from dotenv import load_dotenv

from agent import ITAgent
from clients import acmecorp, healthsync, faststart

load_dotenv()

# Client registry
CLIENTS = {
    "AcmeCorp": acmecorp.get_config(),
    "HealthSync": healthsync.get_config(),
    "FastStart Inc": faststart.get_config()
}


class ChatGUI:
    """Simple chat interface for IT Support Agent."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("IT Support Agent")
        self.root.geometry("800x650")
        self.root.configure(bg="#ffffff")
        
        self.agent = None
        self.current_config = None
        
        # Setup UI
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the user interface."""
        # Header frame with modern styling
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="IT Support Agent",
            font=("Segoe UI", 18, "bold"),
            bg="#2c3e50",
            fg="#ffffff"
        )
        title_label.pack(pady=(15, 5))
        
        # Subtitle with status
        self.status_label = tk.Label(
            header_frame,
            text="",
            font=("Segoe UI", 10),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        self.status_label.pack()
        
        # Client selection frame
        client_frame = tk.Frame(self.root, bg="#ecf0f1", height=60)
        client_frame.pack(fill=tk.X)
        client_frame.pack_propagate(False)
        
        # Inner container for centering
        inner_frame = tk.Frame(client_frame, bg="#ecf0f1")
        inner_frame.pack(expand=True)
        
        tk.Label(
            inner_frame,
            text="Select Client:",
            font=("Segoe UI", 11, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.client_var = tk.StringVar()
        
        # Style the combobox
        style = ttk.Style()
        style.configure("Modern.TCombobox", font=("Segoe UI", 10))
        
        self.client_dropdown = ttk.Combobox(
            inner_frame,
            textvariable=self.client_var,
            values=list(CLIENTS.keys()),
            state="readonly",
            width=25,
            style="Modern.TCombobox",
            font=("Segoe UI", 10)
        )
        self.client_dropdown.pack(side=tk.LEFT)
        self.client_dropdown.current(0)
        self.client_dropdown.bind("<<ComboboxSelected>>", self._on_client_change)
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg="#ffffff")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Chat display area with modern styling
        self.chat_display = scrolledtext.ScrolledText(
            content_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            bg="#ffffff",
            fg="#2c3e50",
            padx=15,
            pady=15,
            state=tk.DISABLED,
            relief=tk.FLAT,
            borderwidth=2,
            highlightthickness=1,
            highlightbackground="#bdc3c7",
            highlightcolor="#3498db"
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for modern styling
        self.chat_display.tag_config("user", foreground="#3498db", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("agent", foreground="#27ae60", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("tool", foreground="#e67e22", font=("Segoe UI", 10, "italic"))
        self.chat_display.tag_config("error", foreground="#e74c3c", font=("Segoe UI", 10))
        self.chat_display.tag_config("admin", foreground="#95a5a6", font=("Segoe UI", 9, "italic"))
        
        # Bottom frame - Input area with modern styling
        bottom_frame = tk.Frame(self.root, bg="#ecf0f1", height=70)
        bottom_frame.pack(fill=tk.X)
        bottom_frame.pack_propagate(False)
        
        # Inner container with padding
        input_container = tk.Frame(bottom_frame, bg="#ecf0f1")
        input_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Input field with modern styling
        self.input_field = tk.Entry(
            input_container,
            font=("Segoe UI", 11),
            bg="#ffffff",
            fg="#2c3e50",
            relief=tk.FLAT,
            borderwidth=2,
            highlightthickness=1,
            highlightbackground="#bdc3c7",
            highlightcolor="#3498db"
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), ipady=8)
        self.input_field.bind("<Return>", lambda e: self._send_message())
        
        # Modern button styling
        button_style = {
            "font": ("Segoe UI", 10, "bold"),
            "relief": tk.FLAT,
            "cursor": "hand2",
            "borderwidth": 0
        }
        
        # Send button
        self.send_button = tk.Button(
            input_container,
            text="Send",
            bg="#3498db",
            fg="#2c3e50",
            activebackground="#2980b9",
            activeforeground="#2c3e50",
            command=self._send_message,
            width=8,
            **button_style
        )
        self.send_button.pack(side=tk.LEFT, ipady=8, padx=(0, 5))
        
        # Clear button
        self.clear_button = tk.Button(
            input_container,
            text="Clear",
            bg="#95a5a6",
            fg="#2c3e50",
            activebackground="#7f8c8d",
            activeforeground="#2c3e50",
            command=self._clear_chat,
            width=8,
            **button_style
        )
        self.clear_button.pack(side=tk.LEFT, ipady=8)
        
        # Initialize agent with first client
        self._initialize_agent()
        
    def _initialize_agent(self):
        """Initialize the agent with selected client."""
        client_name = self.client_var.get()
        self.current_config = CLIENTS[client_name]
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            self._add_message("System", "Error: OPENAI_API_KEY not found in environment.", "error")
            return
        
        self.agent = ITAgent(
            client_config=self.current_config,
            api_key=api_key
        )
        
        # Welcome message
        self._clear_chat_display()
        welcome = f"Hello! I'm {self.current_config.agent_name}, your IT support assistant.\n"
        welcome += f"How can I help you today?"
        self._add_message(self.current_config.agent_name, welcome, "agent")
        
        # Admin view - tools list (for demo purposes only)
        admin_info = f"\n(Admin View - Available Tools: {', '.join(self.current_config.allowed_tools)})"
        self._add_message("System", admin_info, "admin")
        
        self.status_label.config(text=f"Connected as {self.current_config.agent_name} • {self.current_config.client_name}")
        
    def _on_client_change(self, event):
        """Handle client selection change."""
        self._initialize_agent()
        
    def _add_message(self, sender, message, tag=""):
        """Add a message to the chat display."""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add sender and message with tag applied to both
        self.chat_display.insert(tk.END, f"{sender}: ", tag)
        self.chat_display.insert(tk.END, f"{message}\n\n", tag)
        
        # Auto-scroll to bottom
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
    def _clear_chat(self):
        """Clear chat history."""
        if self.agent:
            self.agent.clear_history()
        self._clear_chat_display()
        self._add_message(
            self.current_config.agent_name,
            "Chat history cleared. How can I help you?",
            "agent"
        )
        
    def _clear_chat_display(self):
        """Clear the chat display."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
    def _send_message(self):
        """Send user message to agent."""
        user_message = self.input_field.get().strip()
        
        if not user_message:
            return
        
        if not self.agent:
            self._add_message("System", "Agent not initialized. Please check your API key.", "error")
            return
        
        # Clear input
        self.input_field.delete(0, tk.END)
        
        # Show user message
        self._add_message("You", user_message, "user")
        
        # Disable input while processing
        self.send_button.config(state=tk.DISABLED)
        self.input_field.config(state=tk.DISABLED)
        self.status_label.config(text="⏳ Processing...")
        
        # Process in background thread
        thread = threading.Thread(target=self._process_message, args=(user_message,))
        thread.daemon = True
        thread.start()
        
    def _process_message(self, user_message):
        """Process message in background thread."""
        try:
            result = self.agent.process(user_message)
            
            # Schedule UI update in main thread
            self.root.after(0, self._handle_response, result)
            
        except Exception as e:
            self.root.after(0, self._handle_error, str(e))
            
    def _handle_response(self, result):
        """Handle agent response in main thread."""
        if result["type"] == "text":
            self._add_message(
                self.current_config.agent_name,
                result["message"],
                "agent"
            )
            
        elif result["type"] == "tool_execution":
            # Show tool execution details
            for tool_result in result["tool_results"]:
                tool_msg = f"🔧 Executing: {tool_result['tool']}\n"
                tool_msg += f"Arguments: {tool_result['arguments']}\n"
                self._add_message("System", tool_msg, "tool")
                
                if tool_result["result"]["success"]:
                    output = tool_result["result"]["output"]
                    if output:
                        self._add_message("Tool Output", output.strip(), "tool")
                else:
                    error = tool_result["result"]["error"]
                    self._add_message("Tool Error", error, "error")
            
            # Show final message
            self._add_message(
                self.current_config.agent_name,
                result["message"],
                "agent"
            )
            
        elif result["type"] == "error":
            self._add_message("Error", result["message"], "error")
        
        # Re-enable input
        self.send_button.config(state=tk.NORMAL)
        self.input_field.config(state=tk.NORMAL)
        self.input_field.focus()
        self.status_label.config(text=f"✓ Connected as {self.current_config.agent_name}")
        
    def _handle_error(self, error_message):
        """Handle error in main thread."""
        self._add_message("Error", error_message, "error")
        self.send_button.config(state=tk.NORMAL)
        self.input_field.config(state=tk.NORMAL)
        self.status_label.config(text="✗ Error occurred")


def main():
    """Launch the GUI."""
    root = tk.Tk()
    app = ChatGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

