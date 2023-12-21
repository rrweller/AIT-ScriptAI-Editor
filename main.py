import tkinter as tk
import json
from tkinter import filedialog, messagebox
from json_parser import read_scriptai_json
from view import Viewport
from line_edit import LineEditor

class ScriptAILineEditorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Autobeam ScriptAI Line Editor")
        
        # Canvas frame for displaying lines
        self.canvas_frame = tk.Frame(master)
        self.canvas_frame.pack(side="left", fill="both", expand=True)
        
        # Side panel frame for buttons and settings
        self.side_panel = tk.Frame(master, bg="lightgrey", width=200)
        self.side_panel.pack(side="right", fill="y", expand=False)
        
        # Create a canvas on which we will display the lines
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", width=800, height=600)
        self.canvas.pack(side="top", fill="both", expand=True)
        
        # Button to load a JSON file
        self.load_button = tk.Button(self.side_panel, text="Load Line JSON", command=self.load_json_dialog)
        self.load_button.pack(pady=10)
        
        # Button to export the JSON File
        self.export_button = tk.Button(self.side_panel, text="Export JSON", command=self.export_json_dialog)
        self.export_button.pack(side=tk.BOTTOM, pady=10)

        # Initialize the viewport for handling the canvas view
        self.viewport = Viewport(self.canvas)

        # Set up the line editor for point editing
        self.line_editor = LineEditor(self.viewport)
        
        # Initialize the path data
        self.path_type = None
        self.path_data = None

    def load_json_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.load_path_data(file_path)
    
    def export_json_dialog(self):
        file_path = filedialog.asksaveasfilename(filetypes=[("JSON files", "*.json")], defaultextension=".json")
        if file_path:
            self.save_edited_path(file_path)

    def load_path_data(self, file_path):
        self.path_type, self.path_data = read_scriptai_json(file_path)
        self.viewport.path_data = self.path_data['path']  # Set the path data for the viewport
        self.viewport.fit_content(self.path_data['path'])  # Fit the content using the viewport

    def save_edited_path(self, file_path):
        try:
            with open(file_path, 'w') as json_file:
                json.dump(self.path_data, json_file, indent=4)
            messagebox.showinfo("Success", "The JSON file has been exported successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScriptAILineEditorApp(root)
    root.after(100, lambda: root.attributes("-topmost", False))  # Ensure the canvas dimensions are updated
    root.mainloop()