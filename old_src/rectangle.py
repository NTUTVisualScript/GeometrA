class Rectangle:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __str__(self):
        return "x:{x}, y:{y}, w:{w}, h:{h}".format(
            x=self.x,
            y=self.y,
            w=self.w,
            h=self.h
        )

    def move_to(self, x, y):
        self.x = x
        self.y = y

    @property
    def center(self):
        return (int(self.x+self.w/2), int(self.y+self.h/2))
