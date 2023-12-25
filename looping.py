class LoopingHandler:
    def __init__(self, point_selector, app):
        self.app = app  # Reference to the LineEditorApp
        self.point_selector = point_selector
        self.start_point = None
        self.end_point = None
        self.waiting_for_start_point = False
        self.waiting_for_end_point = False

    def select_start_point(self):
        selected_index = self.point_selector.selected_point
        if selected_index is not None:
            self.set_start_point(selected_index)
            return True
        else:
            self.waiting_for_start_point = True
            return False

    def select_end_point(self):
        selected_index = self.point_selector.selected_point
        if selected_index is not None:
            self.set_end_point(selected_index)
            return True
        else:
            self.waiting_for_end_point = True
            return False

    def set_start_point(self, index):
        self.start_point = self.point_selector.viewport.path_data[index]
        print(f"Start Point Selected: {self.start_point}")
        self.waiting_for_start_point = False
        self.app.update_button_states()

    def set_end_point(self, index):
        self.end_point = self.point_selector.viewport.path_data[index]
        print(f"End Point Selected: {self.end_point}")
        self.waiting_for_end_point = False
        self.app.update_button_states()

    def check_pending_selection(self, selected_index):
        if self.waiting_for_start_point:
            self.set_start_point(selected_index)
        elif self.waiting_for_end_point:
            self.set_end_point(selected_index)
