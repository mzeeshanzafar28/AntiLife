import customtkinter as ctk
import threading
import string
from tkinter import filedialog
from modules.wordlist_generator import generate_wordlist_logic

class WordlistFrame(ctk.CTkFrame):
    def __init__(self, master, bg_color, text_color, accent_green, accent_red):
        super().__init__(master, fg_color="transparent")
        
        self.accent_green = accent_green
        self.accent_red = accent_red
        self.running = False
        
        # Grid Config
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Title
        self.title = ctk.CTkLabel(self, text="Create Wordlist", 
                                  font=ctk.CTkFont(size=24, weight="bold"),
                                  text_color=accent_green)
        self.title.grid(row=0, column=0, columnspan=2, pady=20, sticky="w")
        
        # Options Frame
        self.opts_frame = ctk.CTkFrame(self, fg_color="#262626")
        self.opts_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=0, pady=10)
        
        # Checkboxes
        self.var_lower = ctk.BooleanVar(value=True)
        self.chk_lower = ctk.CTkCheckBox(self.opts_frame, text="Lowercase (a-z)", variable=self.var_lower,
                                         fg_color=accent_red, hover_color=accent_green)
        self.chk_lower.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.var_upper = ctk.BooleanVar(value=False)
        self.chk_upper = ctk.CTkCheckBox(self.opts_frame, text="Uppercase (A-Z)", variable=self.var_upper,
                                         fg_color=accent_red, hover_color=accent_green)
        self.chk_upper.grid(row=0, column=1, padx=20, pady=10, sticky="w")
        
        self.var_nums = ctk.BooleanVar(value=True)
        self.chk_nums = ctk.CTkCheckBox(self.opts_frame, text="Numbers (0-9)", variable=self.var_nums,
                                         fg_color=accent_red, hover_color=accent_green)
        self.chk_nums.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.var_special = ctk.BooleanVar(value=False)
        self.chk_special = ctk.CTkCheckBox(self.opts_frame, text="Special Symbols", variable=self.var_special,
                                         fg_color=accent_red, hover_color=accent_green)
        self.chk_special.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        
        # Custom specific chars
        self.lbl_custom = ctk.CTkLabel(self.opts_frame, text="Custom Chars:")
        self.lbl_custom.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.entry_custom = ctk.CTkEntry(self.opts_frame, placeholder_text="e.g. @#$")
        self.entry_custom.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        
        # Length
        self.len_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.len_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        
        self.lbl_min = ctk.CTkLabel(self.len_frame, text="Min Length:")
        self.lbl_min.grid(row=0, column=0, padx=20, sticky="w")
        self.entry_min = ctk.CTkEntry(self.len_frame, width=50)
        self.entry_min.insert(0, "4")
        self.entry_min.grid(row=0, column=1, padx=10)
        
        self.lbl_max = ctk.CTkLabel(self.len_frame, text="Max Length:")
        self.lbl_max.grid(row=0, column=2, padx=20, sticky="w")
        self.entry_max = ctk.CTkEntry(self.len_frame, width=50)
        self.entry_max.insert(0, "6")
        self.entry_max.grid(row=0, column=3, padx=10)
        
        # Output File
        self.file_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.file_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)
        
        self.btn_file = ctk.CTkButton(self.file_frame, text="Select Output File", command=self.select_file,
                                      fg_color="#3c3c3c", hover_color="#505050")
        self.btn_file.pack(side="left", padx=20)
        
        self.lbl_file = ctk.CTkLabel(self.file_frame, text="No file selected", text_color="gray")
        self.lbl_file.pack(side="left", padx=10)
        
        # Actions
        self.btn_start = ctk.CTkButton(self, text="GENERATE WORDLIST", command=self.start_generation,
                                       fg_color=accent_red, hover_color="#cc0000", height=50,
                                       font=ctk.CTkFont(size=18, weight="bold"))
        self.btn_start.grid(row=4, column=0, columnspan=2, sticky="ew", padx=20, pady=20)
        
        # Progress
        self.lbl_status = ctk.CTkLabel(self, text="Ready", text_color=accent_green)
        self.lbl_status.grid(row=5, column=0, columnspan=2)
        
        self.output_path = None

    def select_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            self.output_path = filename
            self.lbl_file.configure(text=filename)

    def start_generation(self):
        if self.running:
            self.running = False
            self.btn_start.configure(text="GENERATE WORDLIST", fg_color=self.accent_red)
            self.lbl_status.configure(text="Stopping...")
            return

        # Validation
        chars = ""
        if self.var_lower.get(): chars += string.ascii_lowercase
        if self.var_upper.get(): chars += string.ascii_uppercase
        if self.var_nums.get(): chars += string.digits
        if self.var_special.get(): chars += string.punctuation
        chars += self.entry_custom.get()
        
        if not chars:
            self.lbl_status.configure(text="Error: No characters selected", text_color=self.accent_red)
            return
            
        try:
            min_l = int(self.entry_min.get())
            max_l = int(self.entry_max.get())
            if min_l > max_l:
                raise ValueError
        except:
            self.lbl_status.configure(text="Error: Invalid length", text_color=self.accent_red)
            return
            
        if not self.output_path:
            self.lbl_status.configure(text="Error: Select output file", text_color=self.accent_red)
            return

        # Start Thread
        self.running = True
        self.btn_start.configure(text="STOP GENERATION", fg_color="#550000")
        self.lbl_status.configure(text="Generating...", text_color=self.accent_green)
        
        thread = threading.Thread(target=self.run_logic, args=(chars, min_l, max_l))
        thread.start()

    def run_logic(self, chars, min_l, max_l):
        status, count = generate_wordlist_logic(chars, min_l, max_l, self.output_path, 
                                                update_callback=self.update_count,
                                                check_stop=lambda: not self.running)
        
        self.after(0, lambda: self.finish_logic(status, count))

    def update_count(self, count):
        # Update UI safely (though ctk is sometimes thread safe, better use after)
        # However, for high frequency updates, we might throttle. 
        # Here just updating label text.
        self.lbl_status.configure(text=f"Generated: {count} words...")

    def finish_logic(self, status, count):
        self.running = False
        self.btn_start.configure(text="GENERATE WORDLIST", fg_color=self.accent_red)
        if status == "Success":
            self.lbl_status.configure(text=f"Completed! Generated {count} words.", text_color=self.accent_green)
        elif status == "Stopped":
            self.lbl_status.configure(text=f"Stopped. Generated {count} words.", text_color="orange")
        else:
            self.lbl_status.configure(text=f"Error: {status}", text_color=self.accent_red)
