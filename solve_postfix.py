from is_float import is_float
def solve_postfix(postfix):
	operators=["+","-","*","/","^"] # List of allowed operators
	def solve_operation(a,b,op): # Solve binary operation
		if op in operators: # Check if the operator can be handled
			a,b=float(a),float(b) # Cast operands
			match op: # Pick operations
				case "+": return a+b # Sum case
				case "-": return a-b # Difference case
				case "*": return a*b # Product case
				case "/": return a/b # Quotient case
				case "^": return a**b # Power case
		else: # Unknown operator
			raise ValueError("Unknown operator")
	stack=[] # Stack for saving operands
	for i in postfix: # Iterate for each position of the list
		if is_float(i): # Operand found
			stack.append(i) # Push to stack
		else: # Operator found
			operand2=stack.pop() # Second operand is the top element of the stack, then pop
			operand1=stack.pop() # First operand is previous to the top, then pop
			stack.append(solve_operation(operand1,operand2,i)) # Push the result to the stack
	return stack[-1] # Last element in stack is the answer
