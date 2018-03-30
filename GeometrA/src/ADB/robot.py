class Robot:
    def key_press(self, keycode):
        raise NotImplementedError("Subclasses should implement this!")

    def key_release(self, keycode):
        raise NotImplementedError("Subclasses should implement this!")

    def send_keys(self, keys):
        raise NotImplementedError("Subclasses should implement this!")

    def drag_and_drop(self, start_x, start_y, end_x, end_y, duration=None):
        raise NotImplementedError("Subclasses should implement this!")

    def capture_screen(self):
        raise NotImplementedError("Subclasses should implement this!")

    def tap(self, x, y, duration):
        raise NotImplementedError("Subclasses should implement this!")

    def swipe(self, start_x, start_y, end_x, end_y, duration):
        raise NotImplementedError("Subclasses should implement this!")

    def pinch(self, x, y, w, h, percent, steps):
        """Pinch on an element a certain amount
        :Args:
         - x, y, w, h - the rect to pinch
         - percent - (optional) amount to pinch.
         - steps - (optional) number of steps in the pinch action
        """
        raise NotImplementedError("Subclasses should implement this!")

    def zoom(self, x, y, w, h, percent, steps):
        """Zoom on an element a certain amount
        :Args:
         - x, y, w, h - the rect to zoom
         - percent - (optional) amount to zoom.
         - steps - (optional) number of steps in the zoom action
        """
        raise NotImplementedError("Subclasses should implement this!")




