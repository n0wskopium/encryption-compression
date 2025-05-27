import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os

# Main application
class FileToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure File Tool")
        self.root.geometry("750x500")
        self.root.configure(bg="#1e1e2f")
        self.root.resizable(True, True)

        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.operation = tk.StringVar(value="encrypt")
        self.password = tk.StringVar()

        self.setup_styles()
        self.build_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#2a2a3d")
        style.configure("TLabel", background="#2a2a3d", foreground="#ffffff", font=("Segoe UI", 10))
        style.configure("TButton", background="#ff4c60", foreground="#ffffff", font=("Segoe UI", 10, "bold"))
        style.configure("TRadiobutton", background="#2a2a3d", foreground="#ffffff")

    def build_ui(self):
        padding = {"padx": 20, "pady": 10}

        ttk.Label(self.root, text="🔐 Secure File Tool", font=("Segoe UI", 18, "bold"), background="#1e1e2f", foreground="white").pack(pady=20)

        frame = ttk.Frame(self.root)
        frame.pack(fill="both", expand=True, **padding)

        # Input file
        ttk.Label(frame, text="Input File:").grid(row=0, column=0, sticky="w")
        entry_input = ttk.Entry(frame, textvariable=self.input_file, width=50)
        entry_input.grid(row=0, column=1, sticky="ew")
        ttk.Button(frame, text="Browse", command=self.browse_input).grid(row=0, column=2, padx=(10, 0))

        # Output file
        ttk.Label(frame, text="Output File:").grid(row=1, column=0, sticky="w")
        entry_output = ttk.Entry(frame, textvariable=self.output_file, width=50)
        entry_output.grid(row=1, column=1, sticky="ew")
        ttk.Button(frame, text="Browse", command=self.browse_output).grid(row=1, column=2, padx=(10, 0))

        # Operation options
        ttk.Label(frame, text="Operation:").grid(row=2, column=0, sticky="nw")
        operations = ["encrypt", "decrypt", "compress", "decompress"]
        for i, op in enumerate(operations):
            ttk.Radiobutton(frame, text=op.capitalize(), variable=self.operation, value=op, command=self.toggle_password).grid(row=2+i, column=1, sticky="w")

        # Password
        self.password_row = ttk.Frame(frame)
        self.password_row.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(20, 0))
        ttk.Label(self.password_row, text="Password:").pack(side="left")
        self.entry_password = ttk.Entry(self.password_row, textvariable=self.password, show="*")
        self.entry_password.pack(side="left", fill="x", expand=True, padx=(10, 0))

        # Run Button
        ttk.Button(self.root, text="🚀 Run Operation", command=self.run_app).pack(pady=20)

        self.toggle_password()

    def toggle_password(self):
        if self.operation.get() in ["encrypt", "decrypt"]:
            self.password_row.grid()
        else:
            self.password_row.grid_remove()

    def browse_input(self):
        file = filedialog.askopenfilename()
        if file:
            self.input_file.set(file)

    def browse_output(self):
        file = filedialog.asksaveasfilename()
        if file:
            self.output_file.set(file)

    def run_app(self):
        input_file = self.input_file.get()
        output_file = self.output_file.get()
        operation = self.operation.get()
        password = self.password.get()

        if not input_file or not output_file:
            messagebox.showerror("Error", "Input and output file must be selected.")
            return

        script_dir = os.path.dirname(os.path.abspath(__file__))

        if operation in ["encrypt", "decrypt"]:
            if not password:
                messagebox.showerror("Error", "Password is required for AES encryption/decryption.")
                return
            exe = os.path.join(script_dir, "encrypt_tool.exe")
            cmd = [exe, operation, input_file, output_file, password]
        else:
            exe = os.path.join(script_dir, "huffman_cli.exe")
            cmd = [exe, operation, input_file, output_file]

        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
            if result.returncode == 0:
                messagebox.showinfo("Success", f"{operation.capitalize()}ion completed successfully.")
            else:
                messagebox.showerror("Error", result.stderr)
        except Exception as e:
            messagebox.showerror("Execution Failed", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FileToolGUI(root)
    root.mainloop()
