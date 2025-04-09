from colorama import init, Fore
init()

class Token:

    token_colors = {"IDENTIFIER": Fore.RED, "INTEGER": Fore.BLUE, "BRACKET": Fore.GREEN, "OPERATION": Fore.YELLOW, "WHITESPACE": Fore.WHITE}

    def __init__(self, token_id, token_value):
        self.token_id = token_id
        self.token_value = token_value

    def __repr__(self):
        return f"{self.token_colors[self.token_id]}{self.token_id} : {self.token_value}{Fore.RESET}"


class Scanner:
    def __init__(self, token_ids):
        self.token_ids = token_ids
        self.index = 0

    def scan_integer(self, expression):
        integer = ""
        while (self.index < len(expression) and
               (expression[self.index] in token_ids["NUMBER"])):

            # Ignore whitespaces between parts of the same integer
            if not expression[self.index] in token_ids["WHITESPACE"]:
                integer += expression[self.index]
            self.index += 1

        return Token("INTEGER", integer)

    def scan_identifier(self, expression):
        identifier = ""
        while (self.index < len(expression) and
               (expression[self.index] in token_ids["LETTER"]
                or expression[self.index] in token_ids["NUMBER"])):

            # Ignore whitespaces between components of an identifier
            if not expression[self.index] in token_ids["WHITESPACE"]:
                identifier += expression[self.index]
            self.index += 1

        return Token("IDENTIFIER", identifier)

    def scan_whitespace(self, expression):
        whitespace = ""
        while self.index < len(expression) and expression[self.index] in token_ids["WHITESPACE"]:
            whitespace += expression[self.index]
            self.index += 1
        return Token("WHITESPACE", whitespace)

    def scanner(self, expression):
        if self.index >= len(expression):
            return None

        # Ignore whitespaces after operators and brackets
        if expression[self.index] in token_ids["WHITESPACE"]:
            return self.scan_whitespace(expression)

        elif expression[self.index] in token_ids["LETTER"]:  # When letter or _ - identifier
            return self.scan_identifier(expression)

        elif expression[self.index] in token_ids["NUMBER"]:  # When digit - integer
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

file_path = 'test_file'

with open(file_path, 'r') as file:
    file_content = file.read()

expression = file_content
print(expression)

token_ids = {"LETTER": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_",
             "NUMBER": "0123456789",
             "BRACKET": "()[]{}",
             "OPERATION": "+-*/",
             "WHITESPACE": " \n\t"}
token_colors = {"IDENTIFIER": "red", "INTEGER": "blue", "BRACKET": "green", "OPERATION": "orange", "WHITESPACE": "black"}

scanner = Scanner(token_ids)

f = open("test_file.html", "w")

while scanner.index < len(expression):
    token = scanner.scanner(expression)
    print(token)
    if token is None:
        break
    if token.token_id == "WHITESPACE":
        temp_whitespace = token.token_value.replace(" ", "&nbsp;")
        temp_whitespace = temp_whitespace.replace("\n", "<br>")
        temp_whitespace = temp_whitespace.replace("\t", "&#9;")
        f.write(temp_whitespace)
    else:
        f.write('<span style="color:' + token_colors[token.token_id] + '">' + token.token_value + '</span>')
f.close()