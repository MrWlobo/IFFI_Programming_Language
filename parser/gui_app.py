import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from tklinenums import TkLineNumbers
import subprocess
import os
import sys

# Add the antlr_output directory to the system path
# This assumes your ANTLR generated files are in a folder named 'antlr_output'
# relative to where you run this script.
script_dir = os.path.dirname(__file__)
antlr_output_dir = os.path.join(script_dir, 'antlr_output')
sys.path.append(antlr_output_dir)

from antlr4 import InputStream, CommonTokenStream
from antlr_output.IffiLexer import IffiLexer
from antlr_output.IffiParser import IffiParser
from CodeGenerator import CodeGenerator


class IffiCompilerGUI:
    def __init__(self, master):
        self.master = master
        with open('./code_samples/working_example.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            self.iffi_code = content

        master.title("IFFI Compiler GUI")

        # --- Layout Configuration ---
        master.grid_rowconfigure(0, weight=1)  # Input area
        master.grid_rowconfigure(1, weight=0)  # Button row
        master.grid_rowconfigure(2, weight=1)  # C Code area
        master.grid_rowconfigure(3, weight=0)  # Output area
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)  # Changed to grid_column_configure

        # --- Iffi Code Input ---
        # --- Iffi Code Input (Top Row, spans both columns) ---
        self.iffi_label = tk.Label(master, text="Iffi Code:")
        self.iffi_label.grid(row=0, column=0, sticky="nw", padx=5, pady=2, columnspan=2)

        # Create a frame for Iffi code and its line numbers
        self.iffi_frame = tk.Frame(master)
        self.iffi_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=(25, 5), columnspan=2)

        self.iffi_text = scrolledtext.ScrolledText(self.iffi_frame, wrap=tk.WORD, width=60, height=20,
                                                   font=("Consolas", 10))
        self.iffi_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)  # Pack into the frame

        # Initialize tklinenums for Iffi code
        self.iffi_linenumbers = TkLineNumbers(self.iffi_frame, self.iffi_text, justify="left",
                                                         colors=("#2192FF", "#FFFFFF"))
        self.iffi_linenumbers.pack(side=tk.LEFT, fill=tk.Y)  # Pack into the frame

        # Link scrolling
        # self.iffi_text.vbar.config(command=self.iffi_linenumbers.redraw)
        self.iffi_linenumbers.bind_all("<MouseWheel>",
                                       lambda event: self.iffi_text.yview_scroll(int(-1 * (event.delta / 120)),
                                                                                 "units"))
        self.iffi_linenumbers.bind_all("<Button-4>", lambda event: self.iffi_text.yview_scroll(-1, "units"))
        self.iffi_linenumbers.bind_all("<Button-5>", lambda event: self.iffi_text.yview_scroll(1, "units"))
        self.iffi_text.bind("<<Modified>>", lambda event: self.iffi_linenumbers.redraw())  # Redraw on text modification
        self.iffi_text.edit_modified(False)  # Reset modified flag initially
        self.iffi_text.insert(tk.END, self.iffi_code)

        # linenums = TkLineNumbers(root, self.iffi_text, justify="center", colors=("#2197db", "#ffffff"))
        # linenums.pack(fill="y", side="left")
        #
        # # Redraw the line numbers when the text widget contents are modified
        # self.iffi_text.bind("<<Modified>>", lambda event: root.after_idle(linenums.redraw), add=True)

        # --- C Code Output ---
        self.c_label = tk.Label(master, text="Generated C Code:")
        self.c_label.grid(row=2, column=0, sticky="nw", padx=5, pady=2)
        self.c_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=60, height=18, font=("Consolas", 10))
        self.c_text.grid(row=2, column=0, sticky="nsew", padx=5, pady=(25, 5))
        self.c_text.config(state=tk.DISABLED)  # Make read-only

        # --- Program Output ---
        self.output_label = tk.Label(master, text="Program Output:")
        self.output_label.grid(row=2, column=1, sticky="nw", padx=5, pady=2)
        self.output_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=60, height=18, font=("Consolas", 10))
        self.output_text.grid(row=2, column=1, sticky="nsew", padx=5, pady=(25, 5))
        self.output_text.config(state=tk.DISABLED)  # Make read-only

        # --- Buttons ---
        self.compile_run_button = tk.Button(master, text="Generate C, Compile & Run", command=self.generate_compile_run)
        self.compile_run_button.grid(row=1, column=0, columnspan=2, pady=10)

        # --- Status Bar ---
        self.status_bar = tk.Label(master, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=3, column=0, columnspan=2, sticky="ew")

    def update_text_area(self, text_widget, content, error=False, linenumbers_widget=None):
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
        text_widget.edit_modified(True)  # Set modified flag to trigger redraw
        if linenumbers_widget:
            linenumbers_widget.redraw()  # Explicitly redraw line numbers
        if error:
            text_widget.config(fg="#f00")

    def generate_compile_run(self):
        self.status_bar.config(text="Processing...")
        self.update_text_area(self.c_text, "")
        self.update_text_area(self.output_text, "")

        iffi_code = self.iffi_text.get(1.0, tk.END).strip()
        if not iffi_code:
            messagebox.showwarning("Input Error", "Please enter Iffi code.")
            self.status_bar.config(text="Ready")
            return

        # --- Step 1: Generate C Code ---
        try:
            input_stream = InputStream(iffi_code)
            lexer = IffiLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = IffiParser(stream)
            tree = parser.start_()

            generator = CodeGenerator()  # Instantiate CodeGenerator
            generator.visit(tree)
            if generator.error is not None:
                self.update_text_area(self.c_text, f"Error [{generator.error[1]}]: {generator.error[0]}", error=True)
                self.status_bar.config(text="Error.")
                return
            else:
                generated_c_code = "\n".join(generator.output)
                self.update_text_area(self.c_text, generated_c_code)
                self.status_bar.config(text="C Code Generated.")

        except Exception as e:
            messagebox.showerror("Code Generation Error", f"An error occurred during C code generation: {e}")
            self.status_bar.config(text="Error")
            return

        # --- Step 2: Save C Code to a temporary file ---
        c_file_name = "temp_iffi_output.c"
        executable_name = "temp_iffi_output"
        if sys.platform == "win32":
            executable_name += ".exe"

        try:
            with open(c_file_name, "w") as f:
                f.write(generated_c_code)
            self.status_bar.config(text=f"C Code saved to {c_file_name}")
        except Exception as e:
            messagebox.showerror("File Write Error", f"Could not write C code to file: {e}")
            self.status_bar.config(text="Error")
            return

        # --- Step 3: Compile C Code ---
        compile_command = ["gcc", c_file_name, "-o", executable_name, "-lm"]  # -lm for math.h functions (like pow)
        self.status_bar.config(text=f"Compiling with: {' '.join(compile_command)}")

        try:
            compile_result = subprocess.run(compile_command, capture_output=True, text=True, check=False)
            if compile_result.returncode != 0:
                error_output = compile_result.stderr
                self.update_text_area(self.output_text, f"Compilation Error:\n{error_output}")
                self.status_bar.config(text="Compilation Failed")
                return
            self.status_bar.config(text="Compilation Successful.")

        except FileNotFoundError:
            messagebox.showerror("Compiler Not Found",
                                 "GCC compiler not found. Please ensure GCC is installed and in your system's PATH.")
            self.status_bar.config(text="Error")
            return
        except Exception as e:
            messagebox.showerror("Compilation Error", f"An unexpected error occurred during compilation: {e}")
            self.status_bar.config(text="Error")
            return

        # --- Step 4: Run Compiled Program ---
        run_command = [f"./{executable_name}"]  # Use ./ for executables on Linux/macOS
        if sys.platform == "win32":
            run_command = [executable_name]  # Just the name on Windows

        self.status_bar.config(text=f"Running program: {' '.join(run_command)}")
        try:
            run_result = subprocess.run(run_command, capture_output=True, text=True, check=False)
            program_output = run_result.stdout + run_result.stderr
            self.update_text_area(self.output_text, program_output)

            if run_result.returncode != 0:
                self.status_bar.config(text=f"Program exited with code {run_result.returncode}")
            else:
                self.status_bar.config(text="Program Ran Successfully.")

        except Exception as e:
            messagebox.showerror("Program Execution Error", f"An error occurred during program execution: {e}")
            self.status_bar.config(text="Error")
        finally:
            # --- Cleanup (Optional) ---
            try:
                if os.path.exists(c_file_name):
                    os.remove(c_file_name)
                if os.path.exists(executable_name):
                    os.remove(executable_name)
            except Exception as e:
                print(f"Cleanup warning: Could not remove temporary files: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = IffiCompilerGUI(root)
    root.mainloop()
