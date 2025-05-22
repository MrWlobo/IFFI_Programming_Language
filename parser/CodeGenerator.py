from antlr_output.IffiVisitor import IffiVisitor
from antlr_output.IffiParser import IffiParser
import os

class CodeGenerator(IffiVisitor):
    def __init__(self):
        self.output = []
        self.for_loop_depth = 0
        self.for_loop_iterables = {}

    def visitStart_(self, ctx: IffiParser.Start_Context):
        libraries = ["stdio.h", "math.h", "stdbool.h", "stdlib.h"]
        for library in libraries:
            self.output.append(f"#include<{library}>")

        folder_path = "advanced_data_types"
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.output.append(content)

        self.output.append("int main() {")
        for stmt_ctx in ctx.statement():
            self.visit(stmt_ctx)
        self.output.append("return 0;")
        self.output.append("}")
        return None

    def visitStatement(self, ctx):
        return self.visit(ctx.getChild(0))

    def visitDeclaration(self, ctx:IffiParser.DeclarationContext):
        var_type = ctx.basic_data_type().getText().lower()
        var_name = ctx.ID().getText()

        if ctx.expr():
            value = self.visit(ctx.expr())
            line = f"{var_type} {var_name} = {value};"
        else:
            advanced_dt = f"{var_type}{ctx.advanced_data_type().getText().lower()}_t"
            line = f"{advanced_dt} {var_name};"
            line += f"{var_name}.next = NULL;"
            if ctx.data_structure():
                for atom in ctx.data_structure().atom():
                    line += f"\n{var_type}Add(&{var_name}, {self.visit(atom)});"
                line += f"\n{advanced_dt}* current_{var_name} = &{var_name};"
                if var_type != "string":
                    line += f"\n{var_type} current_{var_name}_data = current_{var_name}->data;\n"
                else:
                    line += f"\nchar* current_{var_name}_data = current_{var_name}->data;\n"

        self.output.append(line)
        return line

    def visitAssignment(self, ctx: IffiParser.AssignmentContext):
        var_name = ctx.ID().getText()
        value = self.visit(ctx.expr())
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

        elif ctx.ID():
            return ctx.ID().getText()

        elif ctx.function_call_expr():
            return self.visit(ctx.function_call_expr())

        elif ctx.prefix_increment_decrement():
            return self.visit(ctx.prefix_increment_decrement())

        elif ctx.postfix_increment_decrement():
            return self.visit(ctx.postfix_increment_decrement())

        elif ctx.getChildCount() == 3:
            left = self.visit(ctx.expr(0))
            right = self.visit(ctx.expr(1))
            op = ctx.getChild(1).getText()

            if op == "**":
                return f"pow({left}, {right})"
            else:
                return f"{left} {op} {right}"

        elif ctx.getChildCount() == 2:
            expr = self.visit(ctx.expr(0))
            op = ctx.getChild(1).getText()
            return f"{expr}{op}"

        elif ctx.LEFT_PAREN():
            return f"({self.visit(ctx.expr(0))})"

        elif ctx.atom() and ctx.T_IN():
            left = self.visit(ctx.atom())
            if ctx.data_structure():
                right = self.visit(ctx.data_structure())
            else:
                right = ctx.ID().getText()
            return f"in({left}, {right}) /* TODO: implement */"

        elif ctx.data_structure():
            return self.visit(ctx.data_structure())

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


        if ctx.data_structure():
            iterable = self.visit(ctx.data_structure())
        else:
            iterable = ctx.ID(1).getText()

        self.for_loop_iterables[var_name] = iterable

        self.output.append(f"for (int {var_name} = 0; {var_name} < {ctx.basic_data_type().getText()}Length(&{iterable}); {var_name}++) {{")
        self.output.append(f"current_{iterable}_data = current_{iterable}->data;\n")
        self.output.append(f"current_{iterable} = current_{iterable}->next;\n")
        self.visit(ctx.block())
        self.output.append("}")
        self.output.append(f"current_{iterable} = &{iterable};")
        self.output.append(f"current_{iterable}_data = current_{iterable}->data;")
        self.for_loop_depth -= 1
        del self.for_loop_iterables[var_name]
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
            return "char*"

    def visitData_structure(self, ctx: IffiParser.Data_structureContext):
        if ctx.LEFT_BRACKET():
            # Lista
            items = [self.visit(child) for child in ctx.atom()]
            return "{" + ", ".join(items) + "}"  # np. {1, 2, 3} — styl C array initializer

        elif ctx.LEFT_BRACE():
            # Słownik
            keys = ctx.atom()[::2]
            values = ctx.atom()[1::2]
            pairs = [f"{self.visit(k)}: {self.visit(v)}" for k, v in zip(keys, values)]
            return "/* map not directly supported in C: " + ", ".join(pairs) + " */"

        elif ctx.LEFT_PAREN():
            # Krotka
            items = [self.visit(child) for child in ctx.atom()]
            return "/* tuple: (" + ", ".join(items) + ") */"

        else:
            return "/* unknown data structure */"

    def visitPrint_call(self, ctx):
        expr_value = self.visit(ctx.expr())
        #  basic printing.
        if self.for_loop_depth > 0:
            expr_list = expr_value.split(" ")
            line = f"printf(\"%d\\n\", "
            for expr in expr_list:
                if expr in self.for_loop_iterables:
                    line += f"current_{self.for_loop_iterables[expr]}_data"
                else:
                    line += expr
            line += ");"
        else:
            line = f"printf(\"%d\\n\", {expr_value});"
        self.output.append(line)
        return line

    def visitFunction(self, ctx:IffiParser.FunctionContext):
        func_name = ctx.ID().getText()
        return_type = self.visit(ctx.basic_data_type()) if ctx.basic_data_type() else "void"

        args = []
        if ctx.argument():
            for arg_ctx in ctx.argument():
                args.append(self.visit(arg_ctx))
        args_str = ", ".join(args)

        self.output.append(f"{return_type} {func_name}({args_str}) {{")
        self.visit(ctx.block())
        self.output.append("}")
        return None

    def visitArgument(self, ctx:IffiParser.ArgumentContext):
        arg_type = self.visit(ctx.basic_data_type())
        arg_name = ctx.ID().getText()
        return f"{arg_type} {arg_name}"

    def visitFunction_call(self, ctx:IffiParser.Function_callContext):
        return self.visit(ctx.function_call_expr())

    def visitFunction_call_expr(self, ctx:IffiParser.Function_call_exprContext):
        func_name = ctx.ID().getText()
        args = []
        if ctx.expr():
            for expr_ctx in ctx.expr():
                args.append(self.visit(expr_ctx))
        args_str = ", ".join(args)
        self.output.append(f"{func_name}({args_str});")
        return None

    def visitIncrement_decrement(self, ctx:IffiParser.Increment_decrementContext):
        return self.visitChildren(ctx)

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

    def visitData_structure(self, ctx:IffiParser.Data_structureContext):
        return "/* TODO: Translate data structure ot C eqvalent */"

    def visitAdvanced_data_type(self, ctx:IffiParser.Advanced_data_typeContext):
        return "/* TODO: Translate advanced data type to C equivalent */"


