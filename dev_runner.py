#!/usr/bin/env python3
"""
Development runner with hot reload for the chess GUI.
Automatically restarts the GUI when source files are modified.
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path

class HotReloader:
    def __init__(self, script_path, watch_files=None):
        self.script_path = script_path
        self.watch_files = watch_files or []
        self.process = None
        self.last_modified = {}
        self.running = True
        
        # Add the main script to watch list
        if script_path not in self.watch_files:
            self.watch_files.append(script_path)
    
    def get_file_modified_time(self, filepath):
        """Get the last modified time of a file."""
        try:
            return os.path.getmtime(filepath)
        except OSError:
            return 0
    
    def check_for_changes(self):
        """Check if any watched files have been modified."""
        for filepath in self.watch_files:
            current_time = self.get_file_modified_time(filepath)
            last_time = self.last_modified.get(filepath, 0)
            
            if current_time > last_time:
                self.last_modified[filepath] = current_time
                return True
        return False
    
    def start_process(self):
        """Start the GUI process."""
        if self.process:
            self.stop_process()
        
        print(f"🚀 Starting {self.script_path}...")
        self.process = subprocess.Popen([sys.executable, self.script_path])
    
    def stop_process(self):
        """Stop the GUI process."""
        if self.process:
            print("Stopping GUI...")
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                print("Force killing process...")
                self.process.kill()
            self.process = None
    
    def run(self):
        """Run the hot reloader."""
        print("Hot Reload Development Server")
        print(f"Watching: {', '.join(self.watch_files)}")
        print("-" * 50)
        
        # Initialize file modification times
        for filepath in self.watch_files:
            self.last_modified[filepath] = self.get_file_modified_time(filepath)
        
        # Start the initial process
        self.start_process()
        
        try:
            while self.running:
                time.sleep(0.5)  # Check every 500ms
                
                if self.check_for_changes():
                    print("Changes detected! Restarting...")
                    self.start_process()
                
                # Check if process is still running
                if self.process and self.process.poll() is not None:
                    print("GUI process ended")
                    break
                    
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.running = False
            self.stop_process()

def main():
    # Files to watch for changes
    watch_files = [
        "chess_gui.py",
        "ChessVar.py"
    ]
    
    # Check if files exist
    missing_files = [f for f in watch_files if not os.path.exists(f)]
    if missing_files:
        print(f"Missing files: {', '.join(missing_files)}")
        return
    
    reloader = HotReloader("chess_gui.py", watch_files)
    reloader.run()

if __name__ == "__main__":
    main()
