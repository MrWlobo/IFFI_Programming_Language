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