class Singleton:
    __single = None
    def __init__(self):
        if Singleton.__single:
            raise Singleton.__single
        Singleton.__single = self

    def getSingleton():
        if not Singleton.__single:
            Singleton.__single = Singleton()
        return Singleton.__single

    def doSomething(self):
        print("do something...XD")
