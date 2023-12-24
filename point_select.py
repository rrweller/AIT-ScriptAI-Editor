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

        # Change the color of the selected point
        point = self.viewport.path_data[point_index]
        self.original_color = point['color']
        point['color'] = self.lighten_color(self.original_color, 0.5)
        self.viewport.draw_point(point, radius=3)
    
    def deselect_point(self):
        if self.selected_point is not None:
            print("Point deselected")
            
            # Restore the original color of the point
            point = self.viewport.path_data[self.selected_point]
            point['color'] = self.original_color
            self.viewport.draw_point(point, radius=3)

            self.selected_point = None

    def lighten_color(self, color, factor):
        # Lighten the given RGB color
        r, g, b = color
        return int(r + (255 - r) * factor), int(g + (255 - g) * factor), int(b + (255 - b) * factor)

    def selection_threshold(self):
        # Determine the threshold radius for selecting a point
        # This can be a fixed value or dynamically based on the zoom level
        return 6 / self.viewport.zoom

    def transform_inverse(self, x, y):
        # Transform screen coordinates to viewport coordinates
        return (x - self.viewport.offset_x) / self.viewport.zoom, (y - self.viewport.offset_y) / self.viewport.zoom