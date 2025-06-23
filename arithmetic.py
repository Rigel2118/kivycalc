# Solve arithmetic expressions
from parse import parse
from infix_to_postfix import infix_to_postfix
from solve_postfix import solve_postfix
def arithmetic(infix): # Solve arithmetic expressions
    parsed_list=parse(infix) # Parse infix input to list form
    postfix=infix_to_postfix(parsed_list) # Convert to postfix
    return solve_postfix(postfix) # Solve the postfix expression
print(arithmetic("2+5.67*(7-9)"))
