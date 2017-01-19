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

# class Client:
#     def __init__(self, ip, name):
#         self.ip = ip
#         self.name = name
#
#         # ... 其它方法...
#
#
# class ClientEvent:
#     pass
#
#
# class ClientQueue:
#     def __init__(self):
#         self.clients = []
#         self.listeners = []
#
#     def addClientListener(self, listener):
#         self.listeners.append(listener)
#
#     def removeClientListener(self, listener):
#         self.listeners.remove(listener)
#
#     def notifyAdded(self, client):
#         event = ClientEvent()
#         event.ip = client.ip
#         event.name = client.name
#         for listener in self.listeners:
#             listener.clientAdded(event)
#
#     def notifyRemoved(self, client):
#         event = ClientEvent()
#         event.ip = client.ip
#         event.name = client.name
#         for listener in self.listeners:
#             listener.clientRemoved(event)
#
#     def add(self, client):
#         self.clients.append(client)
#         self.notifyAdded(client)
#
#     def remove(self, client):
#         self.clients.remove(client)
#         self.notifyRemoved(client)
#
#         # 還有一些客戶管理佇列的其它職責....
#
#
# class ClientLogger:
#     def clientAdded(self, event):
#         print(event.ip + " added...")
#
#     def clientRemoved(self, event):
#         print(event.ip + " removed...")
#
#
# queue = ClientQueue()
# queue.addClientListener(ClientLogger())
# queue.addClientListener(ClientLogger())
# c1 = Client("127.0.0.1", "caterpillar")
# c2 = Client("192.168.0.2", "justin")
# c3 = Client("192.168.1.255", "ewqasd")
# queue.add(c1)
# queue.add(c2)
# queue.add(c3)