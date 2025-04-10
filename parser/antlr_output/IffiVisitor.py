# Generated from Iffi.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .IffiParser import IffiParser
else:
    from IffiParser import IffiParser

# This class defines a complete generic visitor for a parse tree produced by IffiParser.

class IffiVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by IffiParser#start_.
    def visitStart_(self, ctx:IffiParser.Start_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#statement.
    def visitStatement(self, ctx:IffiParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#declaration.
    def visitDeclaration(self, ctx:IffiParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#assignment.
    def visitAssignment(self, ctx:IffiParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#if_statement.
    def visitIf_statement(self, ctx:IffiParser.If_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#while_loop.
    def visitWhile_loop(self, ctx:IffiParser.While_loopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#do_while_loop.
    def visitDo_while_loop(self, ctx:IffiParser.Do_while_loopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#block.
    def visitBlock(self, ctx:IffiParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#expr.
    def visitExpr(self, ctx:IffiParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#basic_data_type.
    def visitBasic_data_type(self, ctx:IffiParser.Basic_data_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#advanced_data_types.
    def visitAdvanced_data_type(self, ctx:IffiParser.Advanced_data_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#atom.
    def visitAtom(self, ctx:IffiParser.AtomContext):
        return self.visitChildren(ctx)



del IffiParser