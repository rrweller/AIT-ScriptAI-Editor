import tkinter as tk

class Viewport:
    def __init__(self, canvas):
        self.canvas = canvas
        self.zoom_scale = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.path_data = []
        self.item_to_index_map = {}  # Maps canvas item IDs to their corresponding index in path_data

        # Bind mouse events for zoom and pan interaction
        self.canvas.bind('<MouseWheel>', self.on_mousewheel)
        self.canvas.bind('<B3-Motion>', self.on_mouse_drag)
        self.canvas.bind('<Button-3>', self.on_mouse_click)

    def on_mousewheel(self, event):
        scale_factor = 1.1
        if event.delta > 0:  # Zoom in
            self.zoom_scale *= scale_factor
        elif event.delta < 0:  # Zoom out
            self.zoom_scale /= scale_factor
        self.redraw()

    def on_mouse_click(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def on_mouse_drag(self, event):
        # Pans the canvas view
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def fit_content(self, points):
        self.path_data = points

        # Reset the zoom scale and pan offsets
        self.zoom_scale = 1.0
        self.offset_x = 0
        self.offset_y = 0

        # Make sure canvas dimensions are up to date
        self.canvas.update_idletasks()
        
        # Skip fitting if there are no points
        if not points:
            return
        
        # Calculate bounding box of points
        min_x = min(point['x'] for point in points)
        max_x = max(point['x'] for point in points)
        min_y = min(point['y'] for point in points)
        max_y = max(point['y'] for point in points)
        
        # Determine the canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Calculate the necessary scale to fit all points
        x_scale = canvas_width / (max_x - min_x) if max_x > min_x else float('inf')
        y_scale = canvas_height / (max_y - min_y) if max_y > min_y else float('inf')
        self.zoom_scale = min(x_scale, y_scale) * 0.9  # Use the smaller scale and add padding

        # Calculate the center point of the bounding box
        center_x = (max_x + min_x) / 2
        center_y = (max_y + min_y) / 2
        
        # Calculate the offset to center the bounding box in the canvas
        self.offset_x = (canvas_width / 2) - (center_x * self.zoom_scale)
        self.offset_y = (canvas_height / 2) - (center_y * self.zoom_scale)

        self.redraw()

    def draw_point(self, x, y, radius=3, color='blue', point_index=None):
        canvas_x = x * self.zoom_scale + self.offset_x
        canvas_y = y * self.zoom_scale + self.offset_y
        item = self.canvas.create_oval(
            canvas_x - radius, canvas_y - radius, 
            canvas_x + radius, canvas_y + radius,
            fill=color,
            tags=('path_point', f'point{point_index}')
        )
        return item

    def redraw(self):
        self.canvas.delete('path_point')
        self.canvas.delete('path_line')
        self.item_to_index_map.clear()

        for i, point in enumerate(self.path_data):
            item = self.draw_point(point['x'], point['y'], radius=3, color='blue', point_index=i)
            self.item_to_index_map[item] = i

        # Redraw all points and lines with the current path data
        if self.path_data:
            for idx in range(len(self.path_data) - 1):
                self.draw_line(self.path_data[idx]['x'], self.path_data[idx]['y'],
                               self.path_data[idx + 1]['x'], self.path_data[idx + 1]['y'])

            for point in self.path_data:
                self.draw_point(point['x'], point['y'])
        print(self.item_to_index_map)
    
    def draw_line(self, x1, y1, x2, y2, color='blue', width=1):
        canvas_x1 = x1 * self.zoom_scale + self.offset_x
        canvas_y1 = y1 * self.zoom_scale + self.offset_y
        canvas_x2 = x2 * self.zoom_scale + self.offset_x
        canvas_y2 = y2 * self.zoom_scale + self.offset_y
        self.canvas.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2, fill=color, width=width, tags='path_line')