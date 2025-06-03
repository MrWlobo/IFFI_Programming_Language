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
from antlr4.error.ErrorListener import ErrorListener
from CodeGenerator import CodeGenerator


class CustomErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors = [] # A list to store all captured error messages

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        """
        This method is called by ANTLR when a syntax error is detected.

        Args:
            recognizer: The parser instance.
            offendingSymbol: The token that caused the syntax error.
            line: The line number where the error occurred.
            column: The column number where the error occurred.
            msg: The error message from ANTLR.
            e: The recognition exception.
        """
        # Format the error message and add it to our list
        self.errors.append(f"Line {line}:{column} {msg}")

class IffiCompilerGUI:
    def __init__(self, master):
        self.master = master
        with open('./code_samples/input2.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            self.iffi_code = content

        master.title("IFFI Compiler GUI")

        # --- Layout Configuration ---
        master.grid_rowconfigure(0, weight=1)  # Input area
        master.grid_rowconfigure(1, weight=0)  # Button row
        master.grid_rowconfigure(2, weight=1)  # C Code area
        master.grid_rowconfigure(3, weight=0)  # Output area
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

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
        self.iffi_text.vbar.config(command=self.iffi_linenumbers.redraw) # Link the scrollbar to redraw
        self.iffi_linenumbers.bind_all("<MouseWheel>",
                                       lambda event: self.iffi_text.yview_scroll(int(-1 * (event.delta / 120)),
                                                                                 "units"))
        self.iffi_linenumbers.bind_all("<Button-4>", lambda event: self.iffi_text.yview_scroll(-1, "units"))
        self.iffi_linenumbers.bind_all("<Button-5>", lambda event: self.iffi_text.yview_scroll(1, "units"))

        # --- NEW BINDINGS FOR AUTOMATIC LINE NUMBER UPDATE ---
        self.iffi_text.bind("<KeyRelease>", lambda event: self.iffi_linenumbers.redraw())
        self.iffi_text.bind("<BackSpace>", lambda event: self.iffi_linenumbers.redraw())
        self.iffi_text.bind("<Return>", lambda event: self.iffi_linenumbers.redraw())
        self.iffi_text.bind("<<Modified>>", lambda event: self.iffi_linenumbers.redraw()) # Keep this for other operations

        self.iffi_text.edit_modified(False)  # Reset modified flag initially
        self.iffi_text.insert(tk.END, self.iffi_code)


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
        # Create a frame for the buttons to better control their layout
        self.button_frame = tk.Frame(master)
        self.button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # Changed button text and command
        self.load_file_button = tk.Button(self.button_frame, text="Load Iffi File", command=self.load_iffi_file)
        self.load_file_button.pack(side=tk.LEFT, padx=5)

        self.compile_run_button = tk.Button(self.button_frame, text="Generate C, Compile & Run", command=self.generate_compile_run)
        self.compile_run_button.pack(side=tk.LEFT, padx=5)


        # --- Status Bar ---
        self.status_bar = tk.Label(master, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=3, column=0, columnspan=2, sticky="ew")

    def update_text_area(self, text_widget, content, error=False, linenumbers_widget=None):
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
        # We don't set edit_modified(True) for output areas as they are read-only
        # and don't have associated line numbers that need redraw based on their content.
        if linenumbers_widget: # This check is good practice, though unlikely to be True for output areas
            linenumbers_widget.redraw() # Explicitly redraw line numbers if associated

        if error:
            text_widget.config(fg="#f00")
        else:
            text_widget.config(fg="#000")

    def load_iffi_file(self):
        """
        Opens a file dialog to select a file and loads its content
        into the iffi_text scrolled text area.
        """
        file_path = filedialog.askopenfilename(
            initialdir="./code_samples",  # Suggests starting in the 'code_samples' directory
            title="Select Iffi File",
            filetypes=(("Iffi files", "*.txt"), ("All files", "*.*"))
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.iffi_text.config(state=tk.NORMAL)
                self.iffi_text.delete(1.0, tk.END)
                self.iffi_text.insert(tk.END, content)
                self.iffi_text.config(state=tk.NORMAL) # Keep it editable after loading
                self.iffi_text.edit_modified(True) # Set modified flag to trigger redraw for `tklinenums`
                self.status_bar.config(text=f"Loaded: {os.path.basename(file_path)}")
                self.iffi_linenumbers.redraw() # Explicitly redraw after loading to be sure
            except Exception as e:
                messagebox.showerror("File Load Error", f"Could not read file: {e}")
                self.status_bar.config(text="File load failed.")


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

            error_listener = CustomErrorListener()
            parser.removeErrorListeners()
            lexer.removeErrorListeners()

            parser.addErrorListener(error_listener)
            lexer.addErrorListener(error_listener)

            tree = parser.start_()

            if error_listener.errors:
                syntax_errors_str = '\n'.join(error_listener.errors)
                self.update_text_area(self.c_text, syntax_errors_str, error=True)
                return

            generator = CodeGenerator()  # Instantiate CodeGenerator
            generator.visit(tree)
            if generator.error:
                self.update_text_area(self.c_text, f"Error [{generator.error[1]}]: {generator.error[0]}", error=True)
                self.status_bar.config(text="Error.")
                return
            else:
                generated_c_code = "\n".join(generator.output)
                self.update_text_area(self.c_text, generated_c_code)
                self.status_bar.config(text="C Code Generated.")

        except Exception as e:
            # messagebox.showerror("Code Generation Error", f"An error occurred during C code generation: {e}")
            self.update_text_area(self.c_text, e, error=True)
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