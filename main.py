import sys
import os

# Ensure the project root is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import customtkinter as ctk
except ImportError:
    print("Error: customtkinter is not installed. Please run 'pip install -r requirements.txt'")
    sys.exit(1)

from gui.app import AntiLifeApp

if __name__ == "__main__":
    app = AntiLifeApp()
    app.mainloop()
