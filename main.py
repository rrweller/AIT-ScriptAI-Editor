import tkinter as tk
import json
from tkinter import filedialog, messagebox
from json_parser import read_scriptai_json
from view import Viewport

class LineEditorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("ScriptAI Line Editor")

        self.setup_ui()
        self.path_data = None

    def setup_ui(self):
        self.create_canvas()
        self.create_side_panel()

    def create_canvas(self):
        self.canvas_frame = tk.Frame(self.master)
        self.canvas_frame.pack(side="left", fill="both", expand=True)
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", width=800, height=600)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.viewport = Viewport(self.canvas)

    def create_side_panel(self):
        self.side_panel = tk.Frame(self.master, bg="lightgrey", width=200)
        self.side_panel.pack(side="right", fill="y", expand=False)
        self.load_button = tk.Button(self.side_panel, text="Load JSON", command=self.load_json)
        self.load_button.pack(pady=10)
        self.export_button = tk.Button(self.side_panel, text="Export JSON", command=self.export_json)
        self.export_button.pack(side=tk.BOTTOM, pady=10)

    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.read_json(file_path)

    def read_json(self, file_path):
        _, self.path_data = read_scriptai_json(file_path)
        self.viewport.set_path_data(self.path_data['path'])

    def export_json(self):
        file_path = filedialog.asksaveasfilename(filetypes=[("JSON files", "*.json")], defaultextension=".json")
        if file_path:
            self.write_json(file_path)

    def write_json(self, file_path):
        try:
            with open(file_path, 'w') as json_file:
                json.dump(self.path_data, json_file, indent=4)
            messagebox.showinfo("Success", "JSON file exported successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LineEditorApp(root)
    root.mainloop()
