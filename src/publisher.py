

class Publisher(object):

    '''
    A superclass that helps with publish/subscribe listeners.
    '''

    def __init__(self, state):
        self.subscribers = []
        self._stateObject = state

    def add_subscriber(self, sub):
        self.subscribers.append(sub)

    def draw(self, canvas):
        pass

    def update(self, dt):
        pass
