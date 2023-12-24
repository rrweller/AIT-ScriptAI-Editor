import tkinter as tk

class Viewport:
    def __init__(self, canvas):
        self.canvas = canvas
        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.path_data = []
        self.bind_events()

    def bind_events(self):
        self.canvas.bind('<MouseWheel>', self.zoom_view)
        self.canvas.bind('<B3-Motion>', self.drag_view)
        self.canvas.bind('<Button-3>', self.start_drag)

    def zoom_view(self, event):
        scale_factor = 1.1

        # Coordinates of the mouse position relative to the canvas
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)

        # Coordinates of the mouse position in the transformed view
        view_x = (canvas_x - self.offset_x) / self.zoom
        view_y = (canvas_y - self.offset_y) / self.zoom

        # Update the zoom
        if event.delta > 0:  # Zoom in
            self.zoom *= scale_factor
        else:  # Zoom out
            self.zoom /= scale_factor

        # Recalculate offsets to keep the mouse point stationary
        self.offset_x = canvas_x - view_x * self.zoom
        self.offset_y = canvas_y - view_y * self.zoom

        self.redraw()

    def start_drag(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def drag_view(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def set_path_data(self, points):
        self.path_data = points
        self.reset_view()
        self.redraw()

    def reset_view(self):
        print("Resetting view...")
        if not self.path_data:
            return
        
        self.canvas.update_idletasks()  # Update the canvas to get the correct dimensions
        # Reset canvas view position to the initial state
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        min_x = min(point['x'] for point in self.path_data)
        max_x = max(point['x'] for point in self.path_data)
        min_y = min(point['y'] for point in self.path_data)
        max_y = max(point['y'] for point in self.path_data)

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        x_scale = canvas_width / (max_x - min_x) if max_x > min_x else 1
        y_scale = canvas_height / (max_y - min_y) if max_y > min_y else 1
        self.zoom = min(x_scale, y_scale) * 0.9
        print(f"Setting zoom to {self.zoom}")

        # Center the line in the canvas
        center_x = (max_x + min_x) / 2
        center_y = (max_y + min_y) / 2
        print(f"Center of line is at x:{center_x}, y:{center_y}")

        self.offset_x = (canvas_width / 2) - (center_x * self.zoom)
        self.offset_y = (canvas_height / 2) - (center_y * self.zoom)
        print(f"Offsetting line to x: {self.offset_x}, y: {self.offset_y}")

    def redraw(self):
        self.canvas.delete("all")
        if not self.path_data:
            return

        for i in range(len(self.path_data) - 1):
            start_point = self.path_data[i]
            end_point = self.path_data[i + 1]
            self.draw_line(start_point, end_point, color=start_point['color'])
            self.draw_point(start_point)

        # Draw the last point
        if self.path_data:
            self.draw_point(self.path_data[-1])

    def draw_point(self, point, radius=3):
        x, y = self.transform(point['x'], point['y'])
        color = point['color']
        rgb_color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=rgb_color, outline='')

    def draw_line(self, start, end, color=(0, 0, 255), width=1):  # Default color blue
        x1, y1 = self.transform(start['x'], start['y'])
        x2, y2 = self.transform(end['x'], end['y'])
        rgb_color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
        self.canvas.create_line(x1, y1, x2, y2, fill=rgb_color, width=width)

    def transform(self, x, y):
        return x * self.zoom + self.offset_x, y * self.zoom + self.offset_y
    
    def transform_inverse(self, x, y):
        # Transform screen coordinates to viewport coordinates
        return (x - self.offset_x) / self.zoom, (y - self.offset_y) / self.zoom