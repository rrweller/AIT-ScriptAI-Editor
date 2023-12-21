# line_edit.py
class LineEditor:
    def __init__(self, viewport):
        self.viewport = viewport
        self.selected_item = None  # Canvas item ID of the selected point
        self.selected_point_index = None  # Index of the selected point in self.viewport.path_data

        # Colors for selected and deselected points
        self.selected_point_color = 'lightblue'  # Color for the selected point
        self.selected_point_original_color = 'blue'  # Default color for points

        # Bind mouse events for point selection and dragging
        self.viewport.canvas.bind('<Button-1>', self.on_canvas_click)
        self.viewport.canvas.bind('<B1-Motion>', self.on_point_drag)

    def on_canvas_click(self, event):
        # Find the closest item to where the user clicked
        item = self.viewport.canvas.find_closest(event.x, event.y)
        item_id = item[0]  # The ID of the canvas item

        # Check if the clicked item corresponds to a point on the path
        if item_id in self.viewport.item_to_index_map:
            self.select_point(item_id)
            print("Point selected")  # Diagnostic print
        else:
            print("Deselecting point")  # Diagnostic print
            self.deselect_point()

    def select_point(self, item_id):
        print(f"Selecting point with item_id: {item_id}")
        # Deselect any previously selected points
        self.deselect_point()

        # Select the new point
        self.selected_item = item_id
        self.selected_point_index = self.viewport.item_to_index_map[item_id]

        # Highlight the selected point
        self.viewport.canvas.itemconfig(self.selected_item, fill=self.selected_point_color, tags=('path_point', 'selected'))

    def deselect_point(self):
        print("Deselecting point")
        if self.selected_item is not None:
            # Reset the color of the previously selected point
            self.viewport.canvas.itemconfig(self.selected_item, fill=self.selected_point_original_color)
            self.viewport.canvas.dtag(self.selected_item, 'selected')

            # Clear the selected item and index
            self.selected_item = None
            self.selected_point_index = None

    def on_point_drag(self, event):
        # If a point is selected, calculate its new position and update path_data
        if self.selected_point_index is not None:
            new_x = (event.x - self.viewport.offset_x) / self.viewport.zoom_scale
            new_y = (event.y - self.viewport.offset_y) / self.viewport.zoom_scale

            # Update the position of the selected point in the viewport's path_data
            self.viewport.path_data[self.selected_point_index]['x'] = new_x
            self.viewport.path_data[self.selected_point_index]['y'] = new_y

            # Redraw the viewport to reflect changes
            self.viewport.redraw()