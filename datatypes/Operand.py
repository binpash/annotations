class Operand:

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self):
        return str(self.name)

    def get_name(self) -> str:
        return self.name

    def contains(self, arg):
        return self.name.__contains__(arg)