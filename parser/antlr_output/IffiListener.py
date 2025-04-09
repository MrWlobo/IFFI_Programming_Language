# Generated from Iffi.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .IffiParser import IffiParser
else:
    from IffiParser import IffiParser

# This class defines a complete listener for a parse tree produced by IffiParser.
class IffiListener(ParseTreeListener):

    # Enter a parse tree produced by IffiParser#start_.
    def enterStart_(self, ctx:IffiParser.Start_Context):
        pass

    # Exit a parse tree produced by IffiParser#start_.
    def exitStart_(self, ctx:IffiParser.Start_Context):
        pass


    # Enter a parse tree produced by IffiParser#statement.
    def enterStatement(self, ctx:IffiParser.StatementContext):
        pass

    # Exit a parse tree produced by IffiParser#statement.
    def exitStatement(self, ctx:IffiParser.StatementContext):
        pass


    # Enter a parse tree produced by IffiParser#assignment.
    def enterAssignment(self, ctx:IffiParser.AssignmentContext):
        pass

    # Exit a parse tree produced by IffiParser#assignment.
    def exitAssignment(self, ctx:IffiParser.AssignmentContext):
        pass


    # Enter a parse tree produced by IffiParser#if_statement.
    def enterIf_statement(self, ctx:IffiParser.If_statementContext):
        pass

    # Exit a parse tree produced by IffiParser#if_statement.
    def exitIf_statement(self, ctx:IffiParser.If_statementContext):
        pass


    # Enter a parse tree produced by IffiParser#block.
    def enterBlock(self, ctx:IffiParser.BlockContext):
        pass

    # Exit a parse tree produced by IffiParser#block.
    def exitBlock(self, ctx:IffiParser.BlockContext):
        pass


    # Enter a parse tree produced by IffiParser#expr.
    def enterExpr(self, ctx:IffiParser.ExprContext):
        pass

    # Exit a parse tree produced by IffiParser#expr.
    def exitExpr(self, ctx:IffiParser.ExprContext):
        pass


    # Enter a parse tree produced by IffiParser#atom.
    def enterAtom(self, ctx:IffiParser.AtomContext):
        pass

    # Exit a parse tree produced by IffiParser#atom.
    def exitAtom(self, ctx:IffiParser.AtomContext):
        pass



del IffiParser