import tkinter as tk
import json
from tkinter import filedialog, messagebox
from json_parser import read_scriptai_json
from view import Viewport
from point_select import PointSelector
from looping import LoopingHandler

class LineEditorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("ScriptAI Line Editor")

        self.setup_ui()
        self.path_data = None

        self.looping_handler = LoopingHandler(self.point_selector, self)
        self.point_selector.looping_handler = self.looping_handler

    def setup_ui(self):
        self.create_canvas()
        self.create_side_panel()

    def create_canvas(self):
        self.canvas_frame = tk.Frame(self.master)
        self.canvas_frame.pack(side="left", fill="both", expand=True)
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", width=800, height=600)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.viewport = Viewport(self.canvas)
        self.point_selector = PointSelector(self.canvas, self.viewport)

    def create_side_panel(self):
        self.side_panel = tk.Frame(self.master, bg="lightgrey", width=200)
        self.side_panel.pack(side="right", fill="y", expand=False)

        self.load_button = tk.Button(self.side_panel, text="Load JSON", command=self.load_json)
        self.load_button.pack(pady=10)

        # Looping Section
        self.create_looping_section()

        self.export_button = tk.Button(self.side_panel, text="Export JSON", command=self.export_json)
        self.export_button.pack(side=tk.BOTTOM, pady=10)

    def create_looping_section(self):
        looping_frame = tk.LabelFrame(self.side_panel, text="Looping", bg="lightgrey")
        looping_frame.pack(padx=10, pady=10, fill="x", expand=True)

        # Start and End Point Toggle Buttons
        self.start_point_var = tk.BooleanVar()
        self.end_point_var = tk.BooleanVar()

        start_point_button = tk.Checkbutton(looping_frame, text="Start Point", var=self.start_point_var,
                                            command=self.toggle_start_point, indicatoron=False, relief="raised")
        start_point_button.pack(side="left", padx=5, pady=5)
        end_point_button = tk.Checkbutton(looping_frame, text="End Point", var=self.end_point_var,
                                          command=self.toggle_end_point, indicatoron=False, relief="raised")
        end_point_button.pack(side="left", padx=5, pady=5)

        # Number of Loops
        loops_frame = tk.Frame(looping_frame, bg="lightgrey")
        loops_frame.pack(padx=5, pady=5, fill="x")
        self.loop_count = tk.IntVar(value=1)
        tk.Button(loops_frame, text="-", command=lambda: self.update_loops(-1)).pack(side="left")
        tk.Entry(loops_frame, textvariable=self.loop_count, width=5).pack(side="left")
        tk.Button(loops_frame, text="+", command=lambda: self.update_loops(1)).pack(side="left")

        # Loop Line Button
        loop_line_button = tk.Button(looping_frame, text="Loop Line")
        loop_line_button.pack(padx=5, pady=5)
    
    def toggle_start_point(self):
        if not self.looping_handler.select_start_point():
            self.start_point_var.set(True)  # Keep the button toggled if no point selected
        self.update_button_states()

    def toggle_end_point(self):
        if not self.looping_handler.select_end_point():
            self.end_point_var.set(True)  # Keep the button toggled if no point selected
        self.update_button_states()

    def update_button_states(self):
        # Update the state of the start and end point buttons based on the looping handler status
        if not self.looping_handler.waiting_for_start_point:
            self.start_point_var.set(False)
        if not self.looping_handler.waiting_for_end_point:
            self.end_point_var.set(False)

    def update_loops(self, change):
        current_value = self.loop_count.get()
        new_value = max(1, current_value + change)  # Ensure the loop count is at least 1
        self.loop_count.set(new_value)

    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.read_json(file_path)

    def read_json(self, file_path):
        _, self.path_data = read_scriptai_json(file_path)

        # Assign a default color to each point
        for point in self.path_data['path']:
            point['color'] = (70, 93, 242)  # Default blue color

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
