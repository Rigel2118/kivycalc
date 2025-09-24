# Solve arithmetic expressions
from parse import parse
from infix_to_postfix import infix_to_postfix
from solve_postfix import solve_postfix
def arithmetic(infix, ANS="", mode="dec", precision=5): # Solve arithmetic expressions
    parsed_list=parse(infix, ANS) # Parse infix input to list form
    postfix=infix_to_postfix(parsed_list) # Convert to postfix
    return solve_postfix(postfix, mode) # Solve the postfix expression
