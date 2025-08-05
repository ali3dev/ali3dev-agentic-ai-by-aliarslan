"""
Multi-Agent System User Interface
Modern, beautiful interface for interacting with the AI team
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import time
from datetime import datetime
import json

# Import the main system
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main_system import MultiAgentSystem

class MultiAgentInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Agent AI System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f2f5')
        
        # Initialize the system
        self.system = MultiAgentSystem()
        self.system.start_session("ui_user")
        
        # Message queue for thread-safe updates
        self.message_queue = queue.Queue()
        
        # UI state
        self.is_processing = False
        self.current_request = ""
        
        self.setup_ui()
        self.setup_styles()
        self.start_message_processor()
    
    def setup_styles(self):
        """Configure modern styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 16, 'bold'),
                       foreground='#1a1a1a',
                       background='#f0f2f5')
        
        style.configure('Header.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground='#2c3e50',
                       background='#f0f2f5')
        
        style.configure('Status.TLabel',
                       font=('Segoe UI', 10),
                       foreground='#7f8c8d',
                       background='#f0f2f5')
        
        style.configure('Success.TLabel',
                       font=('Segoe UI', 10),
                       foreground='#27ae60',
                       background='#f0f2f5')
        
        style.configure('Error.TLabel',
                       font=('Segoe UI', 10),
                       foreground='#e74c3c',
                       background='#f0f2f5')
    
    def setup_ui(self):
        """Create the main UI layout"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Header
        self.create_header(main_frame)
        
        # Main content area
        self.create_main_content(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Create the header section"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        # Title
        title_label = ttk.Label(header_frame, 
                               text="Multi-Agent AI System",
                               style='Title.TLabel')
        title_label.pack(side="left")
        
        # Agent status indicators
        status_frame = ttk.Frame(header_frame)
        status_frame.pack(side="right")
        
        self.agent_status_labels = {}
        agents = ['Manager', 'Researcher', 'Writer', 'Critic', 'Analyst']
        for i, agent in enumerate(agents):
            label = ttk.Label(status_frame,
                             text=f"Agent {agent}",
                             style='Status.TLabel')
            label.grid(row=0, column=i, padx=5)
            self.agent_status_labels[agent] = label
    
    def create_main_content(self, parent):
        """Create the main content area"""
        # Left panel - Input and controls
        left_frame = ttk.Frame(parent)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        # Right panel - Output and history
        right_frame = ttk.Frame(parent)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        
        # Configure weights
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=2)
        left_frame.grid_rowconfigure(2, weight=1)
        right_frame.grid_rowconfigure(1, weight=1)
        
        self.create_input_panel(left_frame)
        self.create_output_panel(right_frame)
    
    def create_input_panel(self, parent):
        """Create the input panel"""
        # Request input section
        input_frame = ttk.LabelFrame(parent, text="Your Request", padding="10")
        input_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Request entry
        self.request_entry = scrolledtext.ScrolledText(input_frame, 
                                                     height=6,
                                                     font=('Segoe UI', 10),
                                                     wrap=tk.WORD)
        self.request_entry.pack(fill="both", expand=True)
        
        # Buttons frame
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        # Submit button
        self.submit_button = ttk.Button(button_frame,
                                       text="Submit Request",
                                       command=self.submit_request,
                                       style='Accent.TButton')
        self.submit_button.pack(side="left", padx=(0, 10))
        
        # Clear button
        clear_button = ttk.Button(button_frame,
                                 text="Clear",
                                 command=self.clear_input)
        clear_button.pack(side="left")
        
        # Quick examples section
        examples_frame = ttk.LabelFrame(parent, text="Quick Examples", padding="10")
        examples_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        examples = [
            "Create an SEO-optimized blog post about renewable energy",
            "Research electric vehicle market trends and write a report",
            "Analyze customer feedback data and provide insights",
            "Write a business plan for a sustainable tech startup"
        ]
        
        for i, example in enumerate(examples):
            btn = ttk.Button(examples_frame,
                            text=f"Example {i+1}",
                            command=lambda ex=example: self.load_example(ex))
            btn.grid(row=i//2, column=i%2, sticky="ew", padx=5, pady=2)
        
        # System controls
        controls_frame = ttk.LabelFrame(parent, text="System Controls", padding="10")
        controls_frame.grid(row=2, column=0, sticky="ew")
        
        # Control buttons
        status_button = ttk.Button(controls_frame,
                                  text="System Status",
                                  command=self.show_system_status)
        status_button.pack(fill="x", pady=2)
        
        reset_button = ttk.Button(controls_frame,
                                 text="Reset Session",
                                 command=self.reset_session)
        reset_button.pack(fill="x", pady=2)
        
        history_button = ttk.Button(controls_frame,
                                   text="View History",
                                   command=self.show_history)
        history_button.pack(fill="x", pady=2)
    
    def create_output_panel(self, parent):
        """Create the output panel"""
        # Output display
        output_frame = ttk.LabelFrame(parent, text="System Response", padding="10")
        output_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        # Response text area
        self.response_text = scrolledtext.ScrolledText(output_frame,
                                                      height=15,
                                                      font=('Segoe UI', 10),
                                                      wrap=tk.WORD,
                                                      state=tk.DISABLED)
        self.response_text.pack(fill="both", expand=True)
        
        # Progress frame
        progress_frame = ttk.Frame(output_frame)
        progress_frame.pack(fill="x", pady=(10, 0))
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready")
        self.progress_label = ttk.Label(progress_frame,
                                       textvariable=self.progress_var,
                                       style='Status.TLabel')
        self.progress_label.pack(side="left")
        
        # Processing indicator
        self.processing_label = ttk.Label(progress_frame,
                                         text="",
                                         style='Status.TLabel')
        self.processing_label.pack(side="right")
        
        # History display
        history_frame = ttk.LabelFrame(parent, text="Recent History", padding="10")
        history_frame.grid(row=1, column=0, sticky="nsew")
        
        # History listbox
        self.history_listbox = tk.Listbox(history_frame,
                                         font=('Segoe UI', 9),
                                         selectmode=tk.SINGLE)
        self.history_listbox.pack(fill="both", expand=True)
        self.history_listbox.bind('<Double-Button-1>', self.load_history_item)
    
    def create_status_bar(self, parent):
        """Create the status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        # Status information
        self.status_var = tk.StringVar(value="System ready")
        status_label = ttk.Label(status_frame,
                                textvariable=self.status_var,
                                style='Status.TLabel')
        status_label.pack(side="left")
        
        # Error count
        self.error_var = tk.StringVar(value="Errors: 0")
        error_label = ttk.Label(status_frame,
                               textvariable=self.error_var,
                               style='Status.TLabel')
        error_label.pack(side="right")
    
    def submit_request(self):
        """Submit the user request"""
        request = self.request_entry.get("1.0", tk.END).strip()
        
        if not request:
            messagebox.showwarning("Empty Request", "Please enter a request before submitting.")
            return
        
        if self.is_processing:
            messagebox.showinfo("Processing", "Please wait for the current request to complete.")
            return
        
        self.current_request = request
        self.is_processing = True
        self.submit_button.config(state="disabled")
        self.progress_var.set("Processing request...")
        self.processing_label.config(text="⏳")
        
        # Add to history
        self.add_to_history(f"User: {request[:50]}...")
        
        # Start processing in background thread
        thread = threading.Thread(target=self.process_request_thread, args=(request,))
        thread.daemon = True
        thread.start()
    
    def process_request_thread(self, request):
        """Process request in background thread"""
        try:
            # Process the request
            response = self.system.process_request(request)
            
            # Queue the response for UI update
            self.message_queue.put(('response', response))
            
        except Exception as e:
            error_msg = f"Error processing request: {str(e)}"
            self.message_queue.put(('error', error_msg))
    
    def start_message_processor(self):
        """Start the message processor for thread-safe UI updates"""
        def process_messages():
            while True:
                try:
                    msg_type, data = self.message_queue.get(timeout=0.1)
                    
                    if msg_type == 'response':
                        self.root.after(0, self.display_response, data)
                    elif msg_type == 'error':
                        self.root.after(0, self.display_error, data)
                    elif msg_type == 'progress':
                        self.root.after(0, self.update_progress, data)
                    
                except queue.Empty:
                    continue
        
        thread = threading.Thread(target=process_messages, daemon=True)
        thread.start()
    
    def display_response(self, response):
        """Display the response in the UI"""
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete("1.0", tk.END)
        
        # Format the response
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_response = f"[{timestamp}] System Response:\n\n{response}\n\n"
        
        self.response_text.insert("1.0", formatted_response)
        self.response_text.config(state=tk.DISABLED)
        
        # Update UI state
        self.is_processing = False
        self.submit_button.config(state="normal")
        self.progress_var.set("Response complete")
        self.processing_label.config(text="Complete")
        
        # Add to history
        self.add_to_history(f"System: Response generated ({len(response)} chars)")
        
        # Update status
        self.status_var.set(f"Last request completed at {timestamp}")
    
    def display_error(self, error_msg):
        """Display error message"""
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete("1.0", tk.END)
        
        timestamp = datetime.now().strftime("%H:%M")
        formatted_error = f"[{timestamp}] Error:\n\n{error_msg}\n\n"
        
        self.response_text.insert("1.0", formatted_error)
        self.response_text.config(state=tk.DISABLED)
        
        # Update UI state
        self.is_processing = False
        self.submit_button.config(state="normal")
        self.progress_var.set("Error occurred")
        self.processing_label.config(text="Error")
        
        # Update status
        self.status_var.set(f"Error at {timestamp}")
    
    def clear_input(self):
        """Clear the input field"""
        self.request_entry.delete("1.0", tk.END)
    
    def load_example(self, example):
        """Load an example request"""
        self.request_entry.delete("1.0", tk.END)
        self.request_entry.insert("1.0", example)
    
    def add_to_history(self, entry):
        """Add entry to history list"""
        timestamp = datetime.now().strftime("%H:%M")
        history_entry = f"[{timestamp}] {entry}"
        
        self.history_listbox.insert(0, history_entry)
        
        # Keep only last 20 entries
        if self.history_listbox.size() > 20:
            self.history_listbox.delete(20, tk.END)
    
    def load_history_item(self, event):
        """Load a history item back to input"""
        selection = self.history_listbox.curselection()
        if selection:
            item = self.history_listbox.get(selection[0])
            # Extract the actual request from history entry
            if "User:" in item:
                request = item.split("User: ")[1].split("...")[0]
                self.request_entry.delete("1.0", tk.END)
                self.request_entry.insert("1.0", request)
    
    def show_system_status(self):
        """Show system status in a new window"""
        status_window = tk.Toplevel(self.root)
        status_window.title("System Status")
        status_window.geometry("600x400")
        status_window.configure(bg='#f0f2f5')
        
        # Get system status
        status = self.system.get_system_status()
        
        # Create status display
        status_text = scrolledtext.ScrolledText(status_window,
                                              font=('Consolas', 10),
                                              wrap=tk.WORD)
        status_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Format status information
        status_info = f"""
Multi-Agent AI System Status
{'='*50}

Session Information:
  - Current Session: {status['session_info']['current_session']}
  - Current User: {status['session_info']['current_user']}
  - Session Active: {status['session_info']['session_active']}

Agent Status:
"""
        
        for agent_name, agent_status in status['agents_status'].items():
            status_info += f"  - {agent_name}: {agent_status.get('tasks_completed', 0)} tasks completed\n"
        
        status_info += f"""
Memory Statistics:
  - Total Facts: {status['memory_stats']['total_facts']}
  - Total Insights: {status['memory_stats']['total_insights']}

Tools Status:
"""
        
        for tool_name, tool_status in status['tools_status'].items():
            status_info += f"  - {tool_name}: {tool_status}\n"
        
        status_info += f"""
Error Tracking:
"""
        
        for error_type, count in status['error_tracking'].items():
            status_info += f"  - {error_type}: {count}\n"
        
        status_text.insert("1.0", status_info)
        status_text.config(state=tk.DISABLED)
    
    def show_history(self):
        """Show conversation history"""
        if not self.system.current_session:
            messagebox.showinfo("No Session", "No active session to show history for.")
            return
        
        history_window = tk.Toplevel(self.root)
        history_window.title("Conversation History")
        history_window.geometry("700x500")
        history_window.configure(bg='#f0f2f5')
        
        # Get conversation history
        context = self.system.conversation_history.get_session_context(self.system.current_session)
        
        # Create history display
        history_text = scrolledtext.ScrolledText(history_window,
                                               font=('Segoe UI', 10),
                                               wrap=tk.WORD)
        history_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Format history
        history_info = f"📜 Conversation History for Session: {self.system.current_session}\n"
        history_info += "="*60 + "\n\n"
        
        for i, msg in enumerate(context['recent_messages'], 1):
            timestamp = msg.get('timestamp', 'Unknown')
            speaker = msg.get('speaker', 'Unknown').title()
            message = msg.get('message', 'No message')
            msg_type = msg.get('message_type', 'general')
            
            history_info += f"[{i}] {timestamp} - {speaker} ({msg_type}):\n"
            history_info += f"{message}\n\n"
            history_info += "-"*40 + "\n\n"
        
        history_text.insert("1.0", history_info)
        history_text.config(state=tk.DISABLED)
    
    def reset_session(self):
        """Reset the current session"""
        if messagebox.askyesno("Reset Session", "Are you sure you want to reset the current session?"):
            self.system.start_session()
            self.status_var.set("Session reset")
            self.history_listbox.delete(0, tk.END)
            self.add_to_history("System: Session reset")
            messagebox.showinfo("Session Reset", "Session has been reset successfully.")

def main():
    """Main function to run the interface"""
    root = tk.Tk()
    app = MultiAgentInterface(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main() 