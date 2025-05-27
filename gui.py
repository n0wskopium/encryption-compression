import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
from tkinter import font
import threading
import time

class ModernFileToolGUI:
    def __init__(self, root):
        self.root = root
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready")
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("🔐 SecureCompress Pro - File Encryption & Compression Tool")
        self.root.geometry("800x650")
        self.root.resizable(True, True)
        self.root.minsize(750, 600)
        
        # Set modern colors
        self.bg_color = "#1a1a2e"
        self.card_color = "#16213e"
        self.accent_color = "#0f3460"
        self.primary_color = "#e94560"
        self.text_color = "#ffffff"
        self.secondary_text = "#b8b8b8"
        
        self.root.configure(bg=self.bg_color)
        
    def setup_styles(self):
        """Configure custom styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure custom styles
        self.style.configure('Card.TFrame', 
                           background=self.card_color,
                           relief='flat',
                           borderwidth=1)
        
        self.style.configure('Modern.TButton',
                           background=self.primary_color,
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           font=('Segoe UI', 10, 'bold'))
        
        self.style.map('Modern.TButton',
                      background=[('active', '#d63447'),
                                ('pressed', '#c62d42')])
        
        self.style.configure('Secondary.TButton',
                           background=self.accent_color,
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           font=('Segoe UI', 9))
        
        self.style.map('Secondary.TButton',
                      background=[('active', '#1e4976'),
                                ('pressed', '#0d2744')])
        
        # Custom fonts
        self.title_font = font.Font(family="Segoe UI", size=24, weight="bold")
        self.heading_font = font.Font(family="Segoe UI", size=14, weight="bold")
        self.body_font = font.Font(family="Segoe UI", size=10)
        
    def create_widgets(self):
        """Create and arrange all widgets"""
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title section
        self.create_title_section(main_container)
        
        # File selection section
        self.create_file_section(main_container)
        
        # Operation selection section
        self.create_operation_section(main_container)
        
        # Password section
        self.create_password_section(main_container)
        
        # Action buttons section
        self.create_action_section(main_container)
        
        # Progress and status section
        self.create_progress_section(main_container)
        
    def create_title_section(self, parent):
        """Create the title and description section"""
        title_frame = tk.Frame(parent, bg=self.bg_color)
        title_frame.pack(fill='x', pady=(0, 30))
        
        # Main title
        title_label = tk.Label(title_frame, 
                             text="🔐 SecureCompress Pro",
                             font=self.title_font,
                             bg=self.bg_color,
                             fg=self.text_color)
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(title_frame,
                                text="Advanced File Encryption & Compression System",
                                font=('Segoe UI', 12),
                                bg=self.bg_color,
                                fg=self.secondary_text)
        subtitle_label.pack(pady=(5, 0))
        
        # Feature badges
        features_frame = tk.Frame(title_frame, bg=self.bg_color)
        features_frame.pack(pady=(15, 0))
        
        badges = ["AES-128 Encryption", "Huffman Compression", "Secure Processing"]
        for badge in badges:
            badge_label = tk.Label(features_frame,
                                 text=badge,
                                 bg=self.accent_color,
                                 fg='white',
                                 font=('Segoe UI', 8, 'bold'),
                                 padx=12,
                                 pady=4)
            badge_label.pack(side='left', padx=5)
            
    def create_file_section(self, parent):
        """Create file input/output selection section"""
        # Card container
        card_frame = ttk.Frame(parent, style='Card.TFrame')
        card_frame.pack(fill='x', pady=(0, 20), ipady=20, ipadx=20)
        
        # Section title
        title_label = tk.Label(card_frame,
                             text="📁 File Selection",
                             font=self.heading_font,
                             bg=self.card_color,
                             fg=self.text_color)
        title_label.pack(anchor='w', pady=(0, 15))
        
        # Input file
        input_frame = tk.Frame(card_frame, bg=self.card_color)
        input_frame.pack(fill='x', pady=(0, 15))
        
        input_label = tk.Label(input_frame,
                             text="Input File:",
                             font=self.body_font,
                             bg=self.card_color,
                             fg=self.text_color)
        input_label.pack(anchor='w', pady=(0, 5))
        
        input_row = tk.Frame(input_frame, bg=self.card_color)
        input_row.pack(fill='x')
        
        self.input_entry = tk.Entry(input_row,
                                  font=self.body_font,
                                  bg='white',
                                  fg='black',
                                  relief='flat',
                                  bd=0,
                                  highlightthickness=1,
                                  highlightcolor=self.primary_color)
        self.input_entry.pack(side='left', fill='x', expand=True, ipady=8, ipadx=10)
        
        input_btn = ttk.Button(input_row,
                             text="Browse",
                             style='Secondary.TButton',
                             command=self.browse_input)
        input_btn.pack(side='right', padx=(10, 0))
        
        # Output file
        output_frame = tk.Frame(card_frame, bg=self.card_color)
        output_frame.pack(fill='x')
        
        output_label = tk.Label(output_frame,
                              text="Output File:",
                              font=self.body_font,
                              bg=self.card_color,
                              fg=self.text_color)
        output_label.pack(anchor='w', pady=(0, 5))
        
        output_row = tk.Frame(output_frame, bg=self.card_color)
        output_row.pack(fill='x')
        
        self.output_entry = tk.Entry(output_row,
                                   font=self.body_font,
                                   bg='white',
                                   fg='black',
                                   relief='flat',
                                   bd=0,
                                   highlightthickness=1,
                                   highlightcolor=self.primary_color)
        self.output_entry.pack(side='left', fill='x', expand=True, ipady=8, ipadx=10)
        
        output_btn = ttk.Button(output_row,
                              text="Browse",
                              style='Secondary.TButton',
                              command=self.browse_output)
        output_btn.pack(side='right', padx=(10, 0))
        
    def create_operation_section(self, parent):
        """Create operation selection section"""
        card_frame = ttk.Frame(parent, style='Card.TFrame')
        card_frame.pack(fill='x', pady=(0, 20), ipady=20, ipadx=20)
        
        title_label = tk.Label(card_frame,
                             text="⚙️ Operation Mode",
                             font=self.heading_font,
                             bg=self.card_color,
                             fg=self.text_color)
        title_label.pack(anchor='w', pady=(0, 15))
        
        self.operation_var = tk.StringVar(value="encrypt")
        
        # Create operation buttons in a grid
        operations_frame = tk.Frame(card_frame, bg=self.card_color)
        operations_frame.pack(fill='x')
        
        operations = [
            ("🔒 Encrypt", "encrypt", "Secure your files with AES-128 encryption"),
            ("🔓 Decrypt", "decrypt", "Decrypt previously encrypted files"),
            ("📦 Compress", "compress", "Reduce file size using Huffman coding"),
            ("📂 Decompress", "decompress", "Restore compressed files to original size")
        ]
        
        for i, (text, value, desc) in enumerate(operations):
            row = i // 2
            col = i % 2
            
            op_frame = tk.Frame(operations_frame, bg=self.card_color)
            op_frame.grid(row=row, column=col, sticky='ew', padx=5, pady=5)
            operations_frame.grid_columnconfigure(col, weight=1)
            
            # Create custom radio button style
            radio_btn = tk.Radiobutton(op_frame,
                                     text=text,
                                     variable=self.operation_var,
                                     value=value,
                                     font=('Segoe UI', 11, 'bold'),
                                     bg=self.card_color,
                                     fg=self.text_color,
                                     selectcolor=self.primary_color,
                                     activebackground=self.card_color,
                                     activeforeground=self.text_color,
                                     command=self.update_password_visibility)
            radio_btn.pack(anchor='w')
            
            desc_label = tk.Label(op_frame,
                                text=desc,
                                font=('Segoe UI', 8),
                                bg=self.card_color,
                                fg=self.secondary_text)
            desc_label.pack(anchor='w', padx=(20, 0))
            
    def create_password_section(self, parent):
        """Create password input section"""
        self.password_card = ttk.Frame(parent, style='Card.TFrame')
        self.password_card.pack(fill='x', pady=(0, 20), ipady=20, ipadx=20)
        
        title_label = tk.Label(self.password_card,
                             text="🔑 Security Key",
                             font=self.heading_font,
                             bg=self.card_color,
                             fg=self.text_color)
        title_label.pack(anchor='w', pady=(0, 15))
        
        password_frame = tk.Frame(self.password_card, bg=self.card_color)
        password_frame.pack(fill='x')
        
        password_label = tk.Label(password_frame,
                                text="Password:",
                                font=self.body_font,
                                bg=self.card_color,
                                fg=self.text_color)
        password_label.pack(anchor='w', pady=(0, 5))
        
        password_row = tk.Frame(password_frame, bg=self.card_color)
        password_row.pack(fill='x')
        
        self.password_entry = tk.Entry(password_row,
                                     show="*",
                                     font=self.body_font,
                                     bg='white',
                                     fg='black',
                                     relief='flat',
                                     bd=0,
                                     highlightthickness=1,
                                     highlightcolor=self.primary_color)
        self.password_entry.pack(side='left', fill='x', expand=True, ipady=8, ipadx=10)
        
        # Toggle password visibility button
        self.show_password_var = tk.BooleanVar()
        show_btn = tk.Checkbutton(password_row,
                                text="Show",
                                variable=self.show_password_var,
                                command=self.toggle_password_visibility,
                                bg=self.card_color,
                                fg=self.text_color,
                                selectcolor=self.card_color,
                                activebackground=self.card_color,
                                activeforeground=self.text_color)
        show_btn.pack(side='right', padx=(10, 0))
        
        # Security note
        note_label = tk.Label(password_frame,
                            text="💡 Use a strong password for better security",
                            font=('Segoe UI', 8),
                            bg=self.card_color,
                            fg=self.secondary_text)
        note_label.pack(anchor='w', pady=(5, 0))
        
    def create_action_section(self, parent):
        """Create action buttons section"""
        action_frame = tk.Frame(parent, bg=self.bg_color)
        action_frame.pack(fill='x', pady=(0, 20))
        
        # Main action button
        self.run_btn = ttk.Button(action_frame,
                                text="🚀 Execute Operation",
                                style='Modern.TButton',
                                command=self.run_app_threaded)
        self.run_btn.pack(side='left', padx=(0, 10), ipadx=20, ipady=10)
        
        # Clear button
        clear_btn = ttk.Button(action_frame,
                             text="🗑️ Clear All",
                             style='Secondary.TButton',
                             command=self.clear_all)
        clear_btn.pack(side='left', ipadx=20, ipady=10)
        
        # Help button
        help_btn = ttk.Button(action_frame,
                            text="❓ Help",
                            style='Secondary.TButton',
                            command=self.show_help)
        help_btn.pack(side='right', ipadx=20, ipady=10)
        
    def create_progress_section(self, parent):
        """Create progress and status section"""
        progress_frame = ttk.Frame(parent, style='Card.TFrame')
        progress_frame.pack(fill='x', ipady=15, ipadx=20)
        
        # Status label
        self.status_label = tk.Label(progress_frame,
                                   textvariable=self.status_var,
                                   font=self.body_font,
                                   bg=self.card_color,
                                   fg=self.text_color)
        self.status_label.pack(anchor='w', pady=(0, 10))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_frame,
                                          variable=self.progress_var,
                                          mode='determinate',
                                          length=400)
        self.progress_bar.pack(fill='x')
        
    def browse_input(self):
        """Browse for input file"""
        filename = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[("All Files", "*.*")]
        )
        if filename:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, filename)
            
    def browse_output(self):
        """Browse for output file"""
        filename = filedialog.asksaveasfilename(
            title="Save Output File As",
            filetypes=[("All Files", "*.*")]
        )
        if filename:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, filename)
            
    def update_password_visibility(self):
        """Show/hide password section based on operation"""
        if self.operation_var.get() in ['encrypt', 'decrypt']:
            self.password_card.pack(fill='x', pady=(0, 20), ipady=20, ipadx=20, before=self.run_btn.master)
        else:
            self.password_card.pack_forget()
            
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
            
    def clear_all(self):
        """Clear all input fields"""
        self.input_entry.delete(0, tk.END)
        self.output_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.operation_var.set("encrypt")
        self.update_password_visibility()
        self.status_var.set("Ready")
        self.progress_var.set(0)
        
    def show_help(self):
        """Show help dialog"""
        help_text = """
🔐 SecureCompress Pro - Help Guide

OPERATIONS:
• Encrypt: Protect files using AES-128 encryption
• Decrypt: Restore encrypted files to original form
• Compress: Reduce file size using Huffman coding
• Decompress: Restore compressed files

USAGE:
1. Select input file using Browse button
2. Choose output location and filename
3. Select desired operation mode
4. For encryption/decryption: Enter password
5. Click Execute Operation

SECURITY TIPS:
• Use strong, unique passwords
• Keep your passwords secure
• Test with non-critical files first

SUPPORTED FILES:
• All file types supported
• No size limitations (memory dependent)
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Help - SecureCompress Pro")
        help_window.geometry("500x400")
        help_window.configure(bg=self.bg_color)
        help_window.transient(self.root)
        help_window.grab_set()
        
        text_widget = tk.Text(help_window,
                            bg=self.card_color,
                            fg=self.text_color,
                            font=('Segoe UI', 10),
                            wrap='word',
                            padx=20,
                            pady=20)
        text_widget.pack(fill='both', expand=True, padx=20, pady=20)
        text_widget.insert('1.0', help_text)
        text_widget.config(state='disabled')
        
    def animate_progress(self):
        """Animate progress bar during operation"""
        for i in range(101):
            self.progress_var.set(i)
            self.root.update_idletasks()
            time.sleep(0.01)
            
    def run_app_threaded(self):
        """Run the application in a separate thread"""
        thread = threading.Thread(target=self.run_app)
        thread.daemon = True
        thread.start()
        
    def run_app(self):
        """Execute the selected operation"""
        input_file = self.input_entry.get()
        output_file = self.output_entry.get()
        operation = self.operation_var.get()
        password = self.password_entry.get()

        if not input_file or not output_file:
            messagebox.showerror("Error", "Please select both input and output files.")
            return

        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Update status
        self.status_var.set(f"Preparing {operation}...")
        self.progress_var.set(0)
        
        # Determine which tool to use
        if operation in ['encrypt', 'decrypt']:
            if not password:
                messagebox.showerror("Error", "Password is required for encryption/decryption.")
                return
            exe = os.path.join(script_dir, "encrypt_tool.exe")
            cmd = [exe, operation, input_file, output_file, password]
        elif operation in ['compress', 'decompress']:
            exe = os.path.join(script_dir, "huffman_cli.exe")
            cmd = [exe, operation, input_file, output_file]
        else:
            messagebox.showerror("Error", "Invalid operation selected.")
            return

        try:
            self.status_var.set(f"Executing {operation}...")
            self.run_btn.config(text="Processing...", state='disabled')
            
            # Animate progress
            self.animate_progress()
            
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if result.returncode == 0:
                self.progress_var.set(100)
                self.status_var.set(f"{operation.capitalize()} completed successfully!")
                messagebox.showinfo("Success", 
                                  f"{operation.capitalize()} completed successfully!\n\n"
                                  f"Output saved to: {output_file}")
            else:
                self.status_var.set(f"{operation.capitalize()} failed!")
                error_msg = result.stderr.decode() if result.stderr else "Unknown error occurred"
                messagebox.showerror("Error", f"Operation failed:\n{error_msg}")
                
        except Exception as e:
            self.status_var.set("Operation failed!")
            messagebox.showerror("Execution Failed", f"An error occurred:\n{str(e)}")
        finally:
            self.run_btn.config(text="🚀 Execute Operation", state='normal')

def main():
    root = tk.Tk()
    app = ModernFileToolGUI(root)
    
    # Initialize password visibility
    app.update_password_visibility()
    
    root.mainloop()

if __name__ == "__main__":
    main()