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

    def scan_integer(self, expression):
        integer = ""
        while (self.index < len(expression) and
               (expression[self.index].isdigit()
                or expression[self.index].isspace())):

            # Ignore whitespaces between parts of the same integer
            if not expression[self.index].isspace():
                integer += expression[self.index]
            self.index += 1

        return Token("INTEGER", integer)

    def scan_identifier(self, expression):
        identifier = ""
        while (self.index < len(expression) and
               (expression[self.index].isalpha()
                or expression[self.index].isdigit()
                or expression[self.index] == "_"
                or expression[self.index].isspace())):

            # Ignore whitespaces between components of an idenifier
            if not expression[self.index].isspace():
                identifier += expression[self.index]
            self.index += 1

        return Token("IDENTIFIER", identifier)

    def scan_whitespace(self, expression):
        while expression[self.index].isspace():
            self.index += 1

    def scanner(self, expression):

        # Ignore whitespaces after operators and brackets
        if expression[self.index].isspace():
            self.scan_whitespace(expression)

        elif expression[self.index].isalpha() or expression[self.index] == "_":  # When letter or _ - identifier
            return self.scan_identifier(expression)

        elif expression[self.index].isdigit():  # When digit - integer
            return self.scan_integer(expression)

        elif expression[self.index] in self.token_ids["BRACKET"]:
            self.index += 1
            return Token("BRACKET", expression[self.index - 1])

        elif expression[self.index] in self.token_ids["OPERATION"]:
            self.index += 1
            return Token("OPERATION", expression[self.index - 1])

        else:
            raise Exception(
                "Scanner error: Unknown character " + expression[self.index] + " in column " + str(self.index))

expression = "ab    (   cd   + 21     5   )  as ds -  * 12 dsa782 (21 fh  32 j    )"

token_ids = {"INTEGER": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], "BRACKET": ["(", ")"],
             "OPERATION": ["+", "-", "*", "/"]}
scanner = Scanner(token_ids)

while scanner.index < len(expression):
    print(scanner.scanner(expression))
