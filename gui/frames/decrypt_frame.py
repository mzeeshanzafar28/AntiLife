import customtkinter as ctk
from modules.decrypt import run_decrypt
from tkinter import filedialog
import threading

class DecryptFrame(ctk.CTkFrame):
    def __init__(self, master, bg_color, text_color, accent_green, accent_red):
        super().__init__(master, fg_color="transparent")
        
        self.lbl_title = ctk.CTkLabel(self, text="Decrypt Handshake", font=ctk.CTkFont(size=24, weight="bold"), text_color=accent_green)
        self.lbl_title.pack(pady=20, anchor="w")
        
        # File Setup
        self.frm_files = ctk.CTkFrame(self, fg_color="#262626")
        self.frm_files.pack(fill="x", pady=10)
        
        self.btn_pcap = ctk.CTkButton(self.frm_files, text="Select .cap/.pcap", command=self.sel_pcap)
        self.btn_pcap.grid(row=0, column=0, padx=10, pady=10)
        self.lbl_pcap = ctk.CTkLabel(self.frm_files, text="None")
        self.lbl_pcap.grid(row=0, column=1, padx=10)
        
        self.btn_word = ctk.CTkButton(self.frm_files, text="Select Wordlist", command=self.sel_word)
        self.btn_word.grid(row=1, column=0, padx=10, pady=10)
        self.lbl_word = ctk.CTkLabel(self.frm_files, text="None")
        self.lbl_word.grid(row=1, column=1, padx=10)
        
        self.entry_bssid = ctk.CTkEntry(self.frm_files, placeholder_text="Target BSSID (Optional)")
        self.entry_bssid.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Start
        self.btn_crack = ctk.CTkButton(self, text="START CRACKING", command=self.start_cracking, fg_color=accent_red)
        self.btn_crack.pack(pady=20, fill="x")
        
        self.txt_out = ctk.CTkTextbox(self)
        self.txt_out.pack(fill="both", expand=True)
        
        self.pcap_path = None
        self.word_path = None

    def sel_pcap(self):
        self.pcap_path = filedialog.askopenfilename(filetypes=[("Capture Files", "*.cap *.pcap *.csv")])
        self.lbl_pcap.configure(text=self.pcap_path)

    def sel_word(self):
        self.word_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        self.lbl_word.configure(text=self.word_path)

    def start_cracking(self):
        if not self.pcap_path or not self.word_path:
            self.txt_out.insert("end", "Error: Select files first.\n")
            return
            
        bssid = self.entry_bssid.get()
        self.btn_crack.configure(state="disabled")
        
        threading.Thread(target=self.run_logic, args=(bssid,)).start()

    def run_logic(self, bssid):
        for line in run_decrypt(self.pcap_path, self.word_path, bssid):
            self.txt_out.insert("end", line)
            self.txt_out.see("end")
        self.btn_crack.configure(state="normal")
