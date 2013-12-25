import publisher
import phys


class InputManager(publisher.Publisher):

    '''
    Allows classes to register to recieve input events
    '''

    def __init__(self, state):
        publisher.Publisher.__init__(self, state)

    def update(self, event):
        publisher.Publisher.update(self, event)
        for subscriber in self.subscribers:
            subscriber.notify(event)
