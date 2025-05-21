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


    # Visit a parse tree produced by IffiParser#loop.
    def visitLoop(self, ctx:IffiParser.LoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#for_loop.
    def visitFor_loop(self, ctx:IffiParser.For_loopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#while_loop.
    def visitWhile_loop(self, ctx:IffiParser.While_loopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#do_while_loop.
    def visitDo_while_loop(self, ctx:IffiParser.Do_while_loopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#function.
    def visitFunction(self, ctx:IffiParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#argument.
    def visitArgument(self, ctx:IffiParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#function_call.
    def visitFunction_call(self, ctx:IffiParser.Function_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#increment_decrement.
    def visitIncrement_decrement(self, ctx:IffiParser.Increment_decrementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#print_call.
    def visitPrint_call(self, ctx:IffiParser.Print_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#try_catch_statement.
    def visitTry_catch_statement(self, ctx:IffiParser.Try_catch_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#stop_statement.
    def visitStop_statement(self, ctx:IffiParser.Stop_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#skip_statement.
    def visitSkip_statement(self, ctx:IffiParser.Skip_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#return_statement.
    def visitReturn_statement(self, ctx:IffiParser.Return_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#block.
    def visitBlock(self, ctx:IffiParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#expr.
    def visitExpr(self, ctx:IffiParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#logic_expr.
    def visitLogic_expr(self, ctx:IffiParser.Logic_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#function_call_expr.
    def visitFunction_call_expr(self, ctx:IffiParser.Function_call_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#prefix_increment_decrement.
    def visitPrefix_increment_decrement(self, ctx:IffiParser.Prefix_increment_decrementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#postfix_increment_decrement.
    def visitPostfix_increment_decrement(self, ctx:IffiParser.Postfix_increment_decrementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#data_structure.
    def visitData_structure(self, ctx:IffiParser.Data_structureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#basic_data_type.
    def visitBasic_data_type(self, ctx:IffiParser.Basic_data_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#advanced_data_type.
    def visitAdvanced_data_type(self, ctx:IffiParser.Advanced_data_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#exception_type.
    def visitException_type(self, ctx:IffiParser.Exception_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IffiParser#atom.
    def visitAtom(self, ctx:IffiParser.AtomContext):
        return self.visitChildren(ctx)



del IffiParser