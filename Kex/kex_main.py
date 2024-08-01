import sys
sys.path.append('C:/Users/HP/Desktop/Python/Projects/Kex')

from kex_lexer import Lexer
from kex_parser import Parser
from kex_interpreter import Interpreter
from kex_tokens import Token, TokenType
from kex_ast import AST, BinOp, Num, Var, Assign, ListExpr, DictExpr
from kex_symbolTable import SymbolTable

def main():
    lexer = Lexer('')
    parser = Parser(lexer)
    interpreter = Interpreter(parser)

    while True:
        try:
            text = input('kex>> ')
            if text.strip().lower() == 'exit':
                break
            if text.strip() == '':
                continue

            lexer.reset(text)
            parser.reset()
            result = interpreter.interpret()

            if result is not None:
                print(result)
        except EOFError:
            print("\nExiting Kex...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == '__main__':
    print("Welcome to Kex! Type 'exit' to quit.")
    main()  # Start the REPL
    print("Goodbye!")
