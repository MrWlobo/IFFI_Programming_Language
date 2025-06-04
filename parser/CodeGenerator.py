from antlr_output.IffiVisitor import IffiVisitor
from antlr_output.IffiParser import IffiParser
import os

class CodeGenerator(IffiVisitor):
    def __init__(self):
        self.output = []
        self.int_main_index = 0
        self.list_types = []
        self.for_loop_depth = 0
        self.for_loop_iterables = {}
        self.var_types = {}
        self.local_var_types = {}
        self.data_structures_count = 0

        self.error = None

    def addDataStructureHandling(self, var_type):
        if var_type in self.list_types:
            return
        folder_path = "advanced_data_types"
        file_path = os.path.join(folder_path, f"{var_type}list.txt")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.output.insert(self.int_main_index, content)
        self.list_types.append(var_type)

    def visitStart_(self, ctx: IffiParser.Start_Context):
        libraries = ["stdio.h", "math.h", "stdbool.h", "stdlib.h"]
        for library in libraries:
            self.output.append(f"#include<{library}>")

        self.int_main_index = len(self.output)
        self.output.append("int main() {")
        for stmt_ctx in ctx.statement():
            self.visit(stmt_ctx)
            if self.error is not None:
                return None
        self.output.append("return 0;")
        self.output.append("}")
        return None

    def visitStatement(self, ctx):
        return self.visit(ctx.getChild(0))

    def visitDeclaration(self, ctx: IffiParser.DeclarationContext):
        var_type = ctx.basic_data_type().getText()
        var_name = ctx.ID().getText()

        if var_name in self.var_types.keys():
            self.error = (f"Cannot declare variable '{var_name}' that already exists.", ctx.ID().symbol.line)

        if ctx.expr():
            value = self.visit(ctx.expr())
            if var_type != "string":
                line = f"{var_type} {var_name} = {value};\n"
            else:
                line = f"char* {var_name} = {value};\n"
            self.var_types[var_name] = var_type
        elif ctx.logic_expr():
            value = self.visit(ctx.logic_expr())
            line = f"{var_type} {var_name} = {value};\n"
            self.var_types[var_name] = var_type
        else:
            self.addDataStructureHandling(var_type)
            advanced_dt = f"{var_type}_{ctx.advanced_data_type().getText().lower()}_t"
            line = f"{advanced_dt} {var_name};\n"
            line += f"{var_name}.next = NULL;"
            self.var_types[var_name] = advanced_dt
            if ctx.data_structure():

                data = self.visit(ctx.data_structure())
                items = data.split()
                if items and items[-1] == "range":
                    items = items[:-1]
                    line += f"\n{var_type}Range(&{var_name}, {items[0]}, {items[1]});"
                    line += f"\n{advanced_dt}* current_{var_name} = &{var_name};"
                    line += f"\n{var_type} current_{var_name}_data = current_{var_name}->data;\n"
                else:
                    items = items[:-1]
                    for item in items:
                        line += f"\n{var_type}Add(&{var_name}, {item});"

                    line += f"\n{advanced_dt}* current_{var_name} = &{var_name};"
                    if var_type != "string":
                        line += f"\n{var_type} current_{var_name}_data = current_{var_name}->data;\n"
                    else:
                        line += f"\nchar* current_{var_name}_data = current_{var_name}->data;\n"

        self.output.append(line)
        return line

    def visitAssignment(self, ctx: IffiParser.AssignmentContext):
        # List element assignment
        if ctx.getChildCount() == 7 and ctx.getChild(1).getText() == "[":
            data_structure_name = ctx.ID().getText()
            index = self.visit(ctx.expr(0))
            value = self.visit(ctx.expr(1))

            basic_data_type = self.var_types[data_structure_name].split("_")[0]
            line = f"{basic_data_type}Modify(&{data_structure_name}, {index}, {value});"
        else:
            # Simple assignment
            var_name = ctx.ID().getText()
            value = self.visit(ctx.expr(0))
            line = f"{var_name} = {value};"

        self.output.append(line)
        return line

    def visitAtom(self, ctx):
        if ctx.INT():
            return ctx.INT().getText()
        elif ctx.FLOAT():
            return ctx.FLOAT().getText()
        elif ctx.BOOL():
            return ctx.BOOL().getText()
        elif ctx.ID():
            return ctx.ID().getText()
        elif ctx.CHAR():
            return ctx.CHAR().getText()
        elif ctx.STRING():
            return ctx.STRING().getText()
        else:
            return "/* unknown atom */"

    def visitExpr(self, ctx: IffiParser.ExprContext):
        if ctx.atom():
            return self.visit(ctx.atom())

        elif ctx.function_call_expr():
            return self.visit(ctx.function_call_expr())

        elif ctx.prefix_increment_decrement():
            return self.visit(ctx.prefix_increment_decrement())

        elif ctx.postfix_increment_decrement():
            return self.visit(ctx.postfix_increment_decrement())

        elif ctx.getChildCount() == 3:
            left = self.visit(ctx.expr(0))
            if left in self.for_loop_iterables:
                left = f"current_{self.for_loop_iterables[left]}_data"
            right = self.visit(ctx.expr(1))
            if right in self.for_loop_iterables:
                right = f"current_{self.for_loop_iterables[right]}_data"
            op = ctx.getChild(1).getText()

            if op == "**":
                return f"(pow( {left} , {right} ))"
            else:
                return f"{left} {op} {right}"

        elif ctx.getChildCount() == 2:
            expr = self.visit(ctx.expr(0))
            if expr in self.for_loop_iterables:
                expr = f"current_{self.for_loop_iterables[expr]}_data"

            op = ctx.getChild(1).getText()
            return f"{expr}{op}"

        elif ctx.LEFT_PAREN():
            return f"({self.visit(ctx.expr(0))})" if ctx.expr(0) not in self.for_loop_iterables else f"current_{self.for_loop_iterables[ctx.expr(0)]}_data"

        elif ctx.atom() and ctx.T_IN():
            left = self.visit(ctx.atom())
            if ctx.data_structure():
                right = self.visit(ctx.data_structure())
            else:
                right = ctx.ID().getText()
            return f"in({left}, {right}) /* TODO: implement */"

        elif ctx.data_structure():
            return self.visit(ctx.data_structure())

        elif ctx.getChildCount() == 4 and ctx.getChild(1).getText() == "[":
            data_structure_name = ctx.getChild(0).getText()
            index = self.visit(ctx.expr(0))
            if index in self.for_loop_iterables:
                return f"current_{self.for_loop_iterables[index]}_data"

            print(self.local_var_types)
            if data_structure_name in self.local_var_types:
                basic_data_type = self.local_var_types[data_structure_name].split("_")[0]
            else:
                basic_data_type = self.var_types[data_structure_name].split("_")[0]
            return f"{basic_data_type}Get(&{data_structure_name}, {index})"

        elif ctx.ID() and ctx.getChildCount() == 1:
            if ctx.ID().getText() in self.for_loop_iterables:
                return f"current_{self.for_loop_iterables[ctx.ID().getText()]}_data"
            return ctx.ID().getText()

        else:
            return "/* Unsupported expr */"

    def visitLogic_expr(self, ctx):
        if ctx.LEFT_PAREN() and ctx.RIGHT_PAREN():
            return f"({self.visit(ctx.logic_expr(0))})"

        if ctx.NOT():
            return f"!{self.visit(ctx.logic_expr(0))}"

        if ctx.AND():
            left = self.visit(ctx.logic_expr(0))
            right = self.visit(ctx.logic_expr(1))
            return f"({left} && {right})"

        if ctx.OR():
            left = self.visit(ctx.logic_expr(0))
            right = self.visit(ctx.logic_expr(1))
            return f"({left} || {right})"

        if ctx.expr(1):
            left = self.visit(ctx.expr(0))
            op = ctx.getChild(1).getText()
            right = self.visit(ctx.expr(1))
            return f"({left} {op} {right})"
        else:
            return self.visit(ctx.expr(0))


    def visitBlock(self, ctx):
        for child in ctx.children:
            self.visit(child)
        return None

    def visitIf_statement(self, ctx):
        # IF
        first_cond = self.visit(ctx.logic_expr(0))
        self.output.append(f"if ({first_cond}) {{")
        self.visit(ctx.block(0))
        self.output.append("}")

        # ELIF
        elif_count = len(ctx.T_ELIF())
        for i in range(elif_count):
            cond = self.visit(ctx.logic_expr(i + 1))
            self.output.append(f"else if ({cond}) {{")
            self.visit(ctx.block(i + 1))
            self.output.append("}")

        # ELSE
        if ctx.T_ELSE():
            self.output.append("else {")
            self.visit(ctx.block(elif_count + 1))
            self.output.append("}")

        return None

    def visitLoop(self, ctx:IffiParser.LoopContext):
        self.output.append("while (true) {")
        self.visit(ctx.block())
        self.output.append("}")

    def visitFor_loop(self, ctx:IffiParser.For_loopContext):
        self.for_loop_depth += 1
        var_type = self.visit(ctx.basic_data_type())
        var_name = ctx.ID(0).getText()

        self.output.append("{")

        # Data structure created in for loops parentheses
        if ctx.data_structure():
            for_data_structure = self.visit(ctx.data_structure())
            elements = for_data_structure.split(" ")
            data_type = elements.pop(-1)

            is_range = False
            if data_type == "range":
                data_type = "list"
                is_range = True

            self.addDataStructureHandling(var_type)

            iterable = f"__temp_{data_type}_{self.data_structures_count}"
            self.data_structures_count += 1
            self.output.append(f"{var_type}_{data_type}_t {iterable};\n{iterable}.next = NULL;")

            if data_type == "list" and not is_range:
                for element in elements:
                    self.output.append(f"\n{var_type}Add(&{iterable}, {element});")

            elif data_type == "list" and is_range:
                self.output.append(f"\n{var_type}Range(&{iterable}, {elements[0]}, {elements[1]});")

            self.output.append(f"\n{var_type}_{data_type}_t* current_{iterable} = &{iterable};")
            self.output.append(f"\n{var_type} current_{iterable}_data = current_{iterable}->data;")

        # Data structure passed as a variable
        else:
            iterable = ctx.ID(1).getText()

        self.for_loop_iterables[var_name] = iterable

        self.output.append(f"for (int {var_name}_idx_temp = 0; {var_name}_idx_temp < {ctx.basic_data_type().getText()}Length(&{iterable}); {var_name}_idx_temp++) {{")
        self.var_types[var_name] = var_type if var_type != "char*" else "string"
        self.output.append(f"{var_type} {var_name} = {var_type}Get(&{iterable}, {var_name}_idx_temp);")
        self.output.append(f"current_{iterable}_data = current_{iterable}->data;\n")
        self.output.append(f"current_{iterable} = current_{iterable}->next;\n")
        self.visit(ctx.block())
        self.output.append("}")
        self.output.append(f"current_{iterable} = &{iterable};")
        self.output.append(f"current_{iterable}_data = current_{iterable}->data;\n}}\n")
        self.for_loop_depth -= 1
        del self.for_loop_iterables[var_name]
        del self.var_types[var_name]
        return None

    def visitWhile_loop(self, ctx:IffiParser.While_loopContext):
        self.output.append(f"while ({self.visit(ctx.logic_expr())}) {{")
        self.visit(ctx.block())
        self.output.append("}")

    def visitDo_while_loop(self, ctx:IffiParser.Do_while_loopContext):
        self.output.append("do {")
        self.visit(ctx.block())
        self.output.append("}")
        self.output.append(f"while ({self.visit(ctx.logic_expr())});")

    def visitBasic_data_type(self, ctx):
        if ctx.TYPE_INT():
            return "int"
        elif ctx.TYPE_FLOAT():
            return "float"
        elif ctx.TYPE_BOOL():
            return "bool"
        elif ctx.TYPE_CHAR():
            return "char"
        elif ctx.TYPE_STRING():
            return "string"
        else:
            return "void"

    def visitData_structure(self, ctx: IffiParser.Data_structureContext):
        if ctx.LEFT_BRACKET():
            # Lista
            items = [self.visit(child) for child in ctx.expr()]
            return " ".join(items) + " list"

        elif ctx.LEFT_BRACE():
            # Słownik
            keys = ctx.atom()[::2]
            values = ctx.atom()[1::2]
            pairs = [f"{self.visit(k)}: {self.visit(v)}" for k, v in zip(keys, values)]
            return "/* map not directly supported in C: " + ", ".join(pairs) + " */"

        if ctx.RANGE():
            start_val = self.visit(ctx.expr(0))
            end_val = self.visit(ctx.expr(1))
            items = [start_val, end_val, "range"]
            return " ".join(items)

        elif ctx.LEFT_PAREN():
            # Krotka
            items = [self.visit(child) for child in ctx.atom()]
            return "/* tuple: (" + ", ".join(items) + ") */"

        else:
            return "/* unknown data structure */"

    def visitPrint_call(self, ctx):
        expr_value = self.visit(ctx.expr())
        if self.error:
            return None

        var_type = None
        # Case 1: Expression is a simple atom (literal or variable ID)
        if ctx.expr().atom():
            atom_ctx = ctx.expr().atom()
            if atom_ctx.INT():
                var_type = "int"
            elif atom_ctx.FLOAT():
                var_type = "float"
            elif atom_ctx.BOOL():
                var_type = "bool"
            elif atom_ctx.CHAR():
                var_type = "char"
            elif atom_ctx.STRING():
                var_type = "string"
            elif atom_ctx.ID():
                var_name = atom_ctx.ID().getText()
                if var_name in self.var_types:
                    var_type = self.var_types[var_name]
                else:
                    self.error = (f"Undeclared variable '{var_name}' used in print statement.",
                                  atom_ctx.ID().symbol.line)
                    return None

        # Case 2: Expression is a variable access (e.g., array[index])
        elif ctx.expr().ID() and ctx.expr().LEFT_BRACKET():
            data_structure_name = ctx.expr().ID().getText()
            if data_structure_name in self.var_types:
                c_adt_type = self.var_types[data_structure_name]
                var_type = c_adt_type.split('_')[0]
            else:
                self.error = (f"Data structure '{data_structure_name}' not declared for print.",
                              ctx.expr().ID().symbol.line)
                return None

        # Case 3: Expression is a function call
        elif ctx.expr().function_call_expr():
            func_name = ctx.expr().function_call_expr().ID().getText()

            # To get the return type, you'd need a symbol table that stores function signatures.
            # For now, we'll make a basic assumption or default.
            # Check if function return type is stored
            if func_name in self.function_return_types:
                var_type = self.function_return_types[func_name]
            else:
                # Default to int for simplicity if function type is unknown
                # In a real compiler, this would be a semantic error or require type inference.
                self.output.append(
                    f"/* Warning: Could not determine return type of function '{func_name}' for print. Defaulting to int. */")
                var_type = "int"

                # Case 4: Expression is a binary operation (e.g., a + b)
        elif (ctx.expr().PLUS() or ctx.expr().MINUS() or ctx.expr().MULTIPLY() or
              ctx.expr().DIVIDE() or ctx.expr().FLOOR_DIVIDE() or ctx.expr().MODULO() or
              ctx.expr().POWER()):
            # This is a very basic heuristic. A proper type system would be needed
            # to determine the result type of 'expr OP expr' based on operand types.
            # For simplicity, if it involves floats, assume float; otherwise int.
            # This requires knowing the *Iffi types* of the operands.
            # For now, let's assume the result of any binary op is int unless a float is explicitly involved.
            # This is hard without a full type system. Let's just default to int for now for binary ops.
            # A more robust approach would be to recursively determine operand types.
            # For this simplified version, we'll assume integer arithmetic unless a float is explicitly involved.
            # If either operand is float, the result is float. Otherwise, it's int.
            # This check is complex without a full type system.
            # For now, we'll default to int for simplicity.
            var_type = "int"  # Simplistic default for binary operations

            # Case 5: Parenthesized expression
        elif ctx.expr().LEFT_PAREN():
            # The type of (expr) is the type of expr. Recursively determine.
            # This is hard without a full type system. Default to int.
            var_type = "int"  # Simplistic default for parenthesized expressions

            # Case 6: Data structure literal (e.g., {1,2,3})
        elif ctx.expr().data_structure():
            # Printing a whole data structure is complex in C (requires custom print functions)
            # We already have logic for this that outputs a comment.
            # Let's ensure it's handled properly.
            # The visit(ctx.expr().data_structure()) already generates a comment.
            self.output.append(
                f"// Cannot directly printf a data structure literal. Use a custom print function if available.")
            return None  # Don't generate printf for this.

            # Case 7: Increment/Decrement (result is the value of the variable)
        elif ctx.expr().prefix_increment_decrement() or ctx.expr().postfix_increment_decrement():
            # The type is the type of the ID being incremented/decremented
            id_name = ctx.expr().ID().getText()  # Assuming ID is directly accessible here
            if id_name in self.var_types:
                var_type = self.var_types[id_name]
            else:
                self.error = (f"Undeclared variable '{id_name}' used in print statement (increment/decrement).",
                              ctx.expr().ID().symbol.line)
                return None

            # Case 8: 'in' operator (returns boolean)
        elif ctx.expr().T_IN():
            var_type = "bool"

            # Fallback for complex or unhandled expressions
        if var_type is None:
            self.output.append(
                f"/* Warning: Could not determine type for print expression: {ctx.expr().getText()}. Defaulting to string. */")
            ffi_type = "string"  # Fallback type

            # Map Iffi type to C printf format specifier
        output_types = {"int": "d", "float": "f", "bool": "d", "char": "c", "string": "s"}
        format_specifier = output_types.get(var_type, "s")  # Default to 's' if type not found

        # Generate the printf call
        # The for_loop_depth and current_iterable_data logic is removed.
        # Loop variables (e.g., 'item' in 'for int item in my_array') are now
        # regular variables in scope due to `TypeGet` assignment, so they are handled
        # by the general `var_type` deduction.
        line = f"printf(\"%{format_specifier}\\n\", {expr_value});"
        self.output.append(line)
        return None

    def visitFunction(self, ctx:IffiParser.FunctionContext):
        func_name = ctx.ID().getText()
        if ctx.basic_data_type():
            return_type = self.visit(ctx.basic_data_type())
        else:
            return_type = "void"

        args = []
        if ctx.argument():
            for arg_ctx in ctx.argument():
                args.append(self.visit(arg_ctx))
                self.local_var_types[self.visit(arg_ctx).split(" ")[1]] = self.visit(arg_ctx).split(" ")[0]
        args_str = ", ".join(args)

        self.output.append(f"{return_type} {func_name}({args_str}) {{")
        self.visit(ctx.block())
        self.output.append("}")
        self.local_var_types = {}

        return None

    def visitArgument(self, ctx:IffiParser.ArgumentContext):
        if ctx.basic_data_type():
            arg_type = self.visit(ctx.basic_data_type())
        else:
            arg_type = self.visit(ctx.advanced_data_type())
        arg_name = ctx.ID().getText()
        return f"{arg_type} {arg_name}"

    def visitFunction_call(self, ctx:IffiParser.Function_callContext):
        self.output.append(f"{self.visit(ctx.function_call_expr())};")
        return self.visit(ctx.function_call_expr())

    def visitFunction_call_expr(self, ctx:IffiParser.Function_call_exprContext):
        func_name = ctx.ID().getText()
        args = []
        if ctx.expr():
            for expr_ctx in ctx.expr():
                args.append(self.visit(expr_ctx))
        args_str = ", ".join(args)
        return f"{func_name}({args_str})"

    def visitIncrement_decrement(self, ctx:IffiParser.Increment_decrementContext):
        if ctx.prefix_increment_decrement():
            self.output.append(self.visit(ctx.prefix_increment_decrement()) + ";")
        elif ctx.postfix_increment_decrement():
            self.output.append(self.visit(ctx.postfix_increment_decrement()) + ";")

    def visitStop_statement(self, ctx:IffiParser.Stop_statementContext):
        self.output.append("break;")
        return "break;"

    def visitSkip_statement(self, ctx:IffiParser.Skip_statementContext):
        self.output.append("continue;")
        return "continue;"

    def visitReturn_statement(self, ctx:IffiParser.Return_statementContext):
        if ctx.logic_expr():
            value = self.visit(ctx.logic_expr())
            self.output.append(f"return {value};")
            return f"return {value};"
        elif ctx.expr():
            value = self.visit(ctx.expr())
            self.output.append(f"return {value};")
            return f"return {value};"
        else:
            self.output.append("return;")
            return "return;"

    def visitPrefix_increment_decrement(self, ctx:IffiParser.Prefix_increment_decrementContext):
        op = ctx.getChild(0).getText()
        id_name = ctx.ID().getText()
        return f"{op}{id_name}"

    def visitPostfix_increment_decrement(self, ctx:IffiParser.Postfix_increment_decrementContext):
        op = ctx.getChild(1).getText()
        id_name = ctx.ID().getText()
        return f"{id_name}{op}"

    # def visitData_structure(self, ctx:IffiParser.Data_structureContext):
    #     return "/* TODO: Translate data structure ot C eqvalent */"

    # def visitAdvanced_data_type(self, ctx:IffiParser.Advanced_data_typeContext):
    #     return "/* TODO: Translate advanced data type to C equivalent */"


