class Token:
    def __init__(self, line, token_type, value):
        self.token_type = token_type
        self.value = value
        self.line = line

    def __eq__(self, other):
        return self.line == other.line and self.token_type == other.token_type and self.value == other.value
    def __str__(self):
        return f'Token({self.line}, "{self.token_type}", "{self.value}")'
    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    pass