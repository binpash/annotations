class Operand:

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self):
        return str(self.name)
