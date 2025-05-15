import sys
from antlr4 import *
from antlr_output.IffiLexer import IffiLexer
from antlr_output.IffiParser import IffiParser
from antlr4.tree.Trees import Trees
from CodeGenerator import CodeGenerator

from VisitorInterp import VisitorInterp

def pretty_print_tree(node, indent=0):
    indent_str = "  " * indent
    node_name = type(node).__name__

    if hasattr(node, 'getText'):
        print(f"{indent_str}{node.__class__.__name__}: {node.getText()}")

    for i in range(node.getChildCount()):
        child = node.getChild(i)
        pretty_print_tree(child, indent + 1)

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = IffiLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = IffiParser(stream)
    tree = parser.start_()
    # print(tree.toStringTree(recog=parser))
    #pretty_print_tree(tree)
    # print(Trees.toStringTree(tree, None, parser))

    generator = CodeGenerator()
    generator.visit(tree)

    with open("output.c", "w", encoding="utf-8") as f:
        # print("Output")
        # print("\n".join(generator.output))
        f.write("\n".join(generator.output))


if __name__ == '__main__':
    main(sys.argv)