class Token:
    def __init__(self, token_id, token_value):
        self.token_id = token_id
        self.token_value = token_value

    def __repr__(self):
        return f"{self.token_id} : {self.token_value}"


class Scanner:
    def __init__(self, token_ids):
        self.token_ids = token_ids
        self.index = 0
        self.tokens = []

    def scan_integer(self, expression):
        start_index = self.index
        integer = ""
        while self.index < len(expression) and expression[self.index].isdigit():
            integer += expression[self.index]
            self.index += 1
        if self.index < len(expression) and (expression[self.index].isalpha() or expression[self.index] == "_"):
            raise Exception(
                "Scanner error: Cannot add literals to integers " + integer + expression[
                    self.index] + " in column " + str(start_index))
        self.tokens.append(Token("INTEGER", integer))

    def scan_identifier(self, expression):
        identifier = ""
        while self.index < len(expression) and (
                expression[self.index].isalpha() or expression[self.index].isdigit() or expression[self.index] == "_"):
            identifier += expression[self.index]
            self.index += 1
        self.tokens.append(Token("IDENTIFIER", identifier))

    def scanner(self, expression):

        if expression[self.index].isspace():  # Ignore whitespaces
            self.index += 1

        elif expression[self.index].isalpha() or expression[self.index] == "_":  # When letter or _ - identifier
            self.scan_identifier(expression)

        elif expression[self.index].isdigit():  # When digit - integer
            self.scan_integer(expression)

        elif expression[self.index] in self.token_ids["BRACKET"]:
            self.tokens.append(Token("BRACKET", expression[self.index]))
            self.index += 1

        elif expression[self.index] in self.token_ids["OPERATION"]:
            self.tokens.append(Token("OPERATION", expression[self.index]))
            self.index += 1

        else:
            raise Exception(
                "Scanner error: Unknown character " + expression[self.index] + " in column " + str(self.index))


expression = "2+3*(76+8/3)+ 3*(9-3)"

token_ids = {"INTEGER": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], "BRACKET": ["(", ")"],
             "OPERATION": ["+", "-", "*", "/"]}
scanner = Scanner(token_ids)

while scanner.index < len(expression):
    scanner.scanner(expression)

print(scanner.tokens)
