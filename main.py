import sys
import tkinter as tk
from main_window import ZeldaRecipesUI
import cli
import os
import shutil
import atexit
import signal
import contextlib
import logging
import time

@contextlib.contextmanager
def cleanup_context():
    try:
        yield
    finally:
        cleanup()

def cleanup():
    print("Running cleanup...")
    folder_path = 'ingredient_images'
    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path, ignore_errors=True)
            print(f"Deleted {folder_path} folder")
        else:
            print(f"{folder_path} folder does not exist")
    except Exception as e:
        print(f"Failed to delete {folder_path}: {str(e)}")
    finally:
        # As a last resort, try to remove the folder using os.system
        os.system(f"rd /s /q {folder_path}")

# Register cleanup function to be called at exit
atexit.register(cleanup)

# Set up signal handlers
def signal_handler(signum, frame):
    print(f"Received signal {signum}")
    cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
    """Entry point for both CLI and GUI versions of the application."""
    global app
    try:
        with cleanup_context():
            if len(sys.argv) > 1 and sys.argv[1] == '--cli':
                cli.main()
            else:
                root = tk.Tk()
                root.report_callback_exception = handle_exception
                app = ZeldaRecipesUI(root)
                root.protocol("WM_DELETE_WINDOW", on_closing)
                root.mainloop()
    finally:
        cleanup()  # Ensure cleanup is called even if an exception occurs

def handle_exception(exc_type, exc_value, exc_traceback):
    print(f"Unhandled exception: {exc_type.__name__}: {exc_value}")
    cleanup()
    sys.exit(1)

def on_closing():
    print("Closing application...")
    if app:
        app.close_resources()
    cleanup()
    root.destroy()
    sys.exit(0)  # Force exit the application

if __name__ == "__main__":
    app = None
    root = None
    main()