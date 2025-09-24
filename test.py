from parse import parse
from infix_to_postfix import infix_to_postfix
from solve_postfix import solve_postfix
from arithmetic import arithmetic
string = "log(34)"
set6 = {"sq", "log", "ln", "sin", "cos", "tan", "asin", "acos", "atan", "exp"} 
print(arithmetic(string, "3", "sci"))
#print(parse(string))

