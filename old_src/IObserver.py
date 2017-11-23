
class  IObserver:

    def update(self,update):
        update()

    def StateUpdate(self,state, buttonstate):
        self.StateUpdate()