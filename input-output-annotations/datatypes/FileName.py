class FileName:

    def __init__(self, name):
        # name should be a string
        self.name = name

    def __repr__(self):
        return str(self.name)

    def __eq__(self, other):
        return self.name == other.name
