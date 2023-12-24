import tkinter as tk

class PointSelector:
    def __init__(self, canvas, viewport):
        self.canvas = canvas
        self.viewport = viewport
        self.selected_point = None
        self.bind_canvas_events()

    def bind_canvas_events(self):
        self.canvas.bind('<Button-1>', self.on_canvas_click)

    def on_canvas_click(self, event):
        # Convert canvas click coordinates to viewport coordinates
        x, y = self.viewport.transform_inverse(event.x, event.y)

        # Find the closest point within a certain radius
        closest_point, min_dist = None, float('inf')
        for i, point in enumerate(self.viewport.path_data):
            dist = ((point['x'] - x) ** 2 + (point['y'] - y) ** 2) ** 0.5
            if dist < min_dist:
                closest_point, min_dist = i, dist

        # Check if a point was close enough to be considered selected
        if min_dist <= self.selection_threshold():
            self.select_point(closest_point)
        else:
            self.deselect_point()

    def select_point(self, point_index):
        if self.selected_point is not None:
            self.deselect_point()

        self.selected_point = point_index
        print(f"Selected point: {self.selected_point}")

        # Additional code to visually indicate selection can be added here

    def deselect_point(self):
        if self.selected_point is not None:
            print("Point deselected")
            self.selected_point = None
            # Additional code to visually update deselection can be added here

    def selection_threshold(self):
        # Determine the threshold radius for selecting a point
        # This can be a fixed value or dynamically based on the zoom level
        return 5 / self.viewport.zoom

    def transform_inverse(self, x, y):
        # Transform screen coordinates to viewport coordinates
        return (x - self.viewport.offset_x) / self.viewport.zoom, (y - self.viewport.offset_y) / self.viewport.zoom