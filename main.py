import sys
import tkinter as tk
from main_window import ZeldaRecipesUI
import cli

def main():
    """Entry point for both CLI and GUI versions of the application."""
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        cli.main()
    else:
        root = tk.Tk()
        app = ZeldaRecipesUI(root)
        root.mainloop()

if __name__ == "__main__":
    main()