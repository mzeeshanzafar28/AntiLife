import customtkinter as ctk
from PIL import Image
import os
from gui.frames.wordlist_frame import WordlistFrame
from gui.frames.handshake_frame import HandshakeFrame
from gui.frames.decrypt_frame import DecryptFrame
from gui.frames.deauth_frame import DeauthFrame
from gui.frames.traffic_frame import TrafficFrame
from gui.frames.ssl_frame import SSLFrame
from gui.frames.osint_frame import OSINTFrame
from gui.frames.eviltwin_frame import EvilTwinFrame
from gui.frames.bluejacking_frame import BluejackingFrame
from gui.frames.jamming_frame import JammingFrame

class AntiLifeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # System Settings
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")

        # Window Configuration
        self.title("The AntiLife Framework")
        self.geometry("1100x700")
        
        # Colors based on HTML
        self.color_bg = "#0e0e0e"
        self.color_text = "#c5c8c6"
        self.color_accent_green = "#00ff00"
        self.color_accent_red = "#ff0000"
        self.color_panel = "#1a1a1a"

        self.configure(fg_color=self.color_bg)

        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=self.color_panel)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(12, weight=1) # Push content up

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="AntiLife\nFramework", 
                                       font=ctk.CTkFont(size=24, weight="bold"),
                                       text_color=self.color_accent_green)
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.author_label = ctk.CTkLabel(self.sidebar_frame, text="By M Zeeshan Zafar",
                                         font=ctk.CTkFont(size=12),
                                         text_color=self.color_accent_red)
        self.author_label.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Navigation Buttons
        self.nav_buttons = {}
        self.frames = {}
        
        self.routes = [
            ("Create Wordlist", "wordlist"),
            ("Capture Handshake", "handshake"),
            ("Decrypt Handshake", "decrypt"),
            ("Deauth Attack", "deauth"),
            ("Traffic Intercept", "traffic"),
            ("SSL Downgrade", "ssl"),
            ("Client MAC OSINT", "osint"),
            ("Evil Twin Attack", "eviltwin"),
            ("Bluejacking", "bluejacking"),
            ("CCTV Jamming", "jamming"),
        ]

        for i, (text, name) in enumerate(self.routes):
            btn = ctk.CTkButton(self.sidebar_frame, text=f"{i+1}. {text}", 
                                command=lambda n=name: self.select_frame(n),
                                fg_color="transparent", text_color=self.color_text,
                                hover_color=self.color_bg, anchor="w")
            btn.grid(row=i+2, column=0, padx=20, pady=5, sticky="ew")
            self.nav_buttons[name] = btn

        # Footer in Sidebar
        self.footer_label = ctk.CTkLabel(self.sidebar_frame, text="v1.0.0", text_color="gray")
        self.footer_label.grid(row=13, column=0, padx=20, pady=20)

        # Main Content Area
        self.init_frames()
        
        # Select first frame
        self.select_frame("wordlist")

    def init_frames(self):
        # Initialize all frames
        self.frames["wordlist"] = WordlistFrame(self, self.color_bg, self.color_text, self.color_accent_green, self.color_accent_red)
        self.frames["handshake"] = HandshakeFrame(self, self.color_bg, self.color_text, self.color_accent_green, self.color_accent_red)
        self.frames["decrypt"] = DecryptFrame(self, self.color_bg, self.color_text, self.color_accent_green, self.color_accent_red)
        self.frames["deauth"] = DeauthFrame(self, self.color_bg, self.color_text, self.color_accent_green, self.color_accent_red)
        self.frames["traffic"] = TrafficFrame(self, self.color_bg, self.color_text, self.color_accent_green, self.color_accent_red)
        self.frames["ssl"] = SSLFrame(self, self.color_bg, self.color_text, self.color_accent_green, self.color_accent_red)
        self.frames["osint"] = OSINTFrame(self, self.color_bg, self.color_text, self.color_accent_green, self.color_accent_red)
        self.frames["eviltwin"] = EvilTwinFrame(self, self.color_bg, self.color_text, self.color_accent_green, self.color_accent_red)
        self.frames["bluejacking"] = BluejackingFrame(self, self.color_bg, self.color_text, self.color_accent_green, self.color_accent_red)
        self.frames["jamming"] = JammingFrame(self, self.color_bg, self.color_text, self.color_accent_green, self.color_accent_red)
        
        # Grid all frames (but only show one at a time via tkraise or grid_forget - grid_forget is better for ctk usually to avoid overlap issues if transparent)
        # Using grid locally in select_frame

    def select_frame(self, name):
        # Update buttons state
        for n, btn in self.nav_buttons.items():
            if n == name:
                 btn.configure(fg_color="#3c3c3c", text_color=self.color_accent_green)
            else:
                 btn.configure(fg_color="transparent", text_color=self.color_text)

        # Show frame
        for n, frame in self.frames.items():
            if n == name:
                frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            else:
                frame.grid_forget()

