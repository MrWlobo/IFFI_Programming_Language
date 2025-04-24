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


    # Enter a parse tree produced by IffiParser#declaration.
    def enterDeclaration(self, ctx:IffiParser.DeclarationContext):
        pass

    # Exit a parse tree produced by IffiParser#declaration.
    def exitDeclaration(self, ctx:IffiParser.DeclarationContext):
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


    # Enter a parse tree produced by IffiParser#for_loop.
    def enterFor_loop(self, ctx:IffiParser.For_loopContext):
        pass

    # Exit a parse tree produced by IffiParser#for_loop.
    def exitFor_loop(self, ctx:IffiParser.For_loopContext):
        pass


    # Enter a parse tree produced by IffiParser#while_loop.
    def enterWhile_loop(self, ctx:IffiParser.While_loopContext):
        pass

    # Exit a parse tree produced by IffiParser#while_loop.
    def exitWhile_loop(self, ctx:IffiParser.While_loopContext):
        pass


    # Enter a parse tree produced by IffiParser#do_while_loop.
    def enterDo_while_loop(self, ctx:IffiParser.Do_while_loopContext):
        pass

    # Exit a parse tree produced by IffiParser#do_while_loop.
    def exitDo_while_loop(self, ctx:IffiParser.Do_while_loopContext):
        pass


    # Enter a parse tree produced by IffiParser#function.
    def enterFunction(self, ctx:IffiParser.FunctionContext):
        pass

    # Exit a parse tree produced by IffiParser#function.
    def exitFunction(self, ctx:IffiParser.FunctionContext):
        pass


    # Enter a parse tree produced by IffiParser#argument.
    def enterArgument(self, ctx:IffiParser.ArgumentContext):
        pass

    # Exit a parse tree produced by IffiParser#argument.
    def exitArgument(self, ctx:IffiParser.ArgumentContext):
        pass


    # Enter a parse tree produced by IffiParser#function_call.
    def enterFunction_call(self, ctx:IffiParser.Function_callContext):
        pass

    # Exit a parse tree produced by IffiParser#function_call.
    def exitFunction_call(self, ctx:IffiParser.Function_callContext):
        pass


    # Enter a parse tree produced by IffiParser#increment_decrement.
    def enterIncrement_decrement(self, ctx:IffiParser.Increment_decrementContext):
        pass

    # Exit a parse tree produced by IffiParser#increment_decrement.
    def exitIncrement_decrement(self, ctx:IffiParser.Increment_decrementContext):
        pass


    # Enter a parse tree produced by IffiParser#try_catch_statement.
    def enterTry_catch_statement(self, ctx:IffiParser.Try_catch_statementContext):
        pass

    # Exit a parse tree produced by IffiParser#try_catch_statement.
    def exitTry_catch_statement(self, ctx:IffiParser.Try_catch_statementContext):
        pass


    # Enter a parse tree produced by IffiParser#stop_statement.
    def enterStop_statement(self, ctx:IffiParser.Stop_statementContext):
        pass

    # Exit a parse tree produced by IffiParser#stop_statement.
    def exitStop_statement(self, ctx:IffiParser.Stop_statementContext):
        pass


    # Enter a parse tree produced by IffiParser#skip_statement.
    def enterSkip_statement(self, ctx:IffiParser.Skip_statementContext):
        pass

    # Exit a parse tree produced by IffiParser#skip_statement.
    def exitSkip_statement(self, ctx:IffiParser.Skip_statementContext):
        pass


    # Enter a parse tree produced by IffiParser#return_statement.
    def enterReturn_statement(self, ctx:IffiParser.Return_statementContext):
        pass

    # Exit a parse tree produced by IffiParser#return_statement.
    def exitReturn_statement(self, ctx:IffiParser.Return_statementContext):
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


    # Enter a parse tree produced by IffiParser#logic_expr.
    def enterLogic_expr(self, ctx:IffiParser.Logic_exprContext):
        pass

    # Exit a parse tree produced by IffiParser#logic_expr.
    def exitLogic_expr(self, ctx:IffiParser.Logic_exprContext):
        pass


    # Enter a parse tree produced by IffiParser#prefix_increment_decrement.
    def enterPrefix_increment_decrement(self, ctx:IffiParser.Prefix_increment_decrementContext):
        pass

    # Exit a parse tree produced by IffiParser#prefix_increment_decrement.
    def exitPrefix_increment_decrement(self, ctx:IffiParser.Prefix_increment_decrementContext):
        pass


    # Enter a parse tree produced by IffiParser#postfix_increment_decrement.
    def enterPostfix_increment_decrement(self, ctx:IffiParser.Postfix_increment_decrementContext):
        pass

    # Exit a parse tree produced by IffiParser#postfix_increment_decrement.
    def exitPostfix_increment_decrement(self, ctx:IffiParser.Postfix_increment_decrementContext):
        pass


    # Enter a parse tree produced by IffiParser#data_structure.
    def enterData_structure(self, ctx:IffiParser.Data_structureContext):
        pass

    # Exit a parse tree produced by IffiParser#data_structure.
    def exitData_structure(self, ctx:IffiParser.Data_structureContext):
        pass


    # Enter a parse tree produced by IffiParser#basic_data_type.
    def enterBasic_data_type(self, ctx:IffiParser.Basic_data_typeContext):
        pass

    # Exit a parse tree produced by IffiParser#basic_data_type.
    def exitBasic_data_type(self, ctx:IffiParser.Basic_data_typeContext):
        pass


    # Enter a parse tree produced by IffiParser#advanced_data_type.
    def enterAdvanced_data_type(self, ctx:IffiParser.Advanced_data_typeContext):
        pass

    # Exit a parse tree produced by IffiParser#advanced_data_type.
    def exitAdvanced_data_type(self, ctx:IffiParser.Advanced_data_typeContext):
        pass


    # Enter a parse tree produced by IffiParser#exception_type.
    def enterException_type(self, ctx:IffiParser.Exception_typeContext):
        pass

    # Exit a parse tree produced by IffiParser#exception_type.
    def exitException_type(self, ctx:IffiParser.Exception_typeContext):
        pass


    # Enter a parse tree produced by IffiParser#atom.
    def enterAtom(self, ctx:IffiParser.AtomContext):
        pass

    # Exit a parse tree produced by IffiParser#atom.
    def exitAtom(self, ctx:IffiParser.AtomContext):
        pass



del IffiParser