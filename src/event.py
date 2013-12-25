class Event(object):

    '''
    Represents an event, eg, a collision taking place
    '''

    def __init__(self, name, reporter, target):
        self.name = name
        self.reporter = reporter
        self.target = target
