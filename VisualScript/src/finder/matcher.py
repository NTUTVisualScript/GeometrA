class Matcher:
    def next(self):
        raise NotImplementedError("Subclasses should implement this!")

    def all(self):
        raise NotImplementedError("Subclasses should implement this!")

