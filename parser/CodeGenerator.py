from antlr_output.IffiVisitor import IffiVisitor
from antlr_output.IffiParser import IffiParser

class CodeGenerator(IffiVisitor):
    def __init__(self):
        self.output = []

    def visitStart_(self, ctx: IffiParser.Start_Context):
        for stmt_ctx in ctx.statement():
            self.visit(stmt_ctx)
        return None

    def visitAssignment(self, ctx: IffiParser.AssignmentContext):
        var_name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        line = f"{var_name} = {value};"
        self.output.append(line)
        return line

    def visitDeclaration(self, ctx:IffiParser.DeclarationContext):
        var_type = ctx.basic_data_type().getText()
        var_name = ctx.ID().getText()

        if ctx.expr():
            value = self.visit(ctx.expr())  # np. "42"
            line = f"{var_type} {var_name} = {value};"
        else:
            line = f"{var_type} {var_name};"

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
        else:
            return "/* unknown atom */"

    def visitExpr(self, ctx: IffiParser.ExprContext):
        if ctx.atom():
            return self.visit(ctx.atom())

        elif ctx.function_call():
            return self.visit(ctx.function_call())

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
                return f"({left} {op} {right})"

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

    def visitStatement(self, ctx):
        return self.visit(ctx.getChild(0))

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

    def visitPrint_call(self, ctx):
        expr_value = self.visit(ctx.expr())
        #  basic printing.
        line = f"printf(\"%d\\n\", {expr_value});"
        self.output.append(line)
        return line