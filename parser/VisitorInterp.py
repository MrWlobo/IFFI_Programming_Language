import sys
from antlr4 import *
from antlr_output.IffiParser import IffiParser
from antlr_output.IffiVisitor import IffiVisitor

class VisitorInterp(IffiVisitor):
    def visitAtom(self, ctx:IffiParser.AtomContext):
        return int(ctx.getText())

    def visitExpr(self, ctx:IffiParser.ExprContext):
        if ctx.getChildCount() == 3:
            if ctx.getChild(0).getText() == "(":
                return self.visit(ctx.getChild(1))
            op = ctx.getChild(1).getText()
            v1 = self.visit(ctx.getChild(0))
            v2 = self.visit(ctx.getChild(2))
            if op == "+":
                return v1 + v2
            if op == "-":
                return v1 - v2
            if op == "*":
                return v1 * v2
            if op == "/":
                return v1 / v2
            return 0
        if ctx.getChildCount() == 2:
            opc = ctx.getChild(0).getText()
            if opc == "+":
                return self.visit(ctx.getChild(1))
            if opc == "-":
                return - self.visit(ctx.getChild(1))
            return 0
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        return 0

    def visitStart_(self, ctx:IffiParser.Start_Context):
        for i in range(0, ctx.getChildCount(), 2):
            print(self.visit(ctx.getChild(i)))
        return 0