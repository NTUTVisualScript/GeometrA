class FindResult:
    def __init__(self, x=0, y=0, w=0, h=0, score=-1):
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)
        self.score = score

    def __str__(self):
        return "x:{x}, y:{y}, w:{w}, h:{h}, score:{score}".format(
            x=self.x,
            y=self.y,
            w=self.w,
            h=self.h,
            score=self.score
        )


