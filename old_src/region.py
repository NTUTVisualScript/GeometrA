from cv2img import Rectangle
from finder.template_finder import TemplateFinder

class Region(Rectangle):
    """
    Region i s a rectangular area on a screen, which is defined by
        1. Its upper left corner (x, y) as a distance relative to the upper left corner of the screen (0, 0) and
        2. Its dimension (w, h) as its width and height
    """

    def __init__(self, x, y, w, h, source_img, screen):
        super().__init__(x, y, w, h)
        self._source_img = source_img
        self._screen = screen

        self._finder = TemplateFinder(self._source_img)

    def find(self, target_img):
        results = self._finder.find_all(target_img, 0.9)

        if results:
            result = results[0]

            return Region(
                result.x,
                result.y,
                result.w,
                result.h,
                self._source_img,
                self._screen)
        else:
            return None

    def click(self):
        return self._screen.click(*self.center)

    def right(self):
        screen_w, screen_h = self._screen.size

        return Region(self.x + self.w,
                      self.y,
                      screen_w - self.x - self.w,
                      self.h,
                      self._source_img,
                      self._screen)

    def left(self):
        return Region(0,
                      self.y,
                      self.x,
                      self.h,
                      self._source_img,
                      self._screen)

    def above(self):
        return Region(self.x,
                      0,
                      self.w,
                      self.y,
                      self._source_img,
                      self._screen)

    def below(self):
        screen_w, screen_h = self._screen.size

        return Region(self.x,
                      self.y + self.h,
                      self.w,
                      screen_h - self.y - self.h,
                      self._source_img,
                      self._screen)

