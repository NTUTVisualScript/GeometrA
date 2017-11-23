class ResultGenerator:
    def next(self):
        raise NotImplementedError("Subclasses should implement this!")

    def __iter__(self):
        return self

    def __next__(self):
        item = self.next()

        if item is None:
            raise StopIteration
        else:
            return item

class Finder:
    def find(self, target_img, *argv):
        raise NotImplementedError("Subclasses should implement this!")

    def find_all(self, target_img, *argv):
        generator = self.find(target_img, *argv)
        return list(map(lambda item: item, generator))
