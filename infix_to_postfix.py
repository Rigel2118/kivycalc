from is_float import is_float

def infix_to_postfix(parsed_list):
	
	precedence={"(":0, "+":1,"-":1,"*":2,"/":2, "C":2, "P":2, "L":2, "%":2, "^":3, "sqrt":4, "cbrt":4, "log":4, "ln":4, "sin":4, "cos":4, "tan":4, "asin":4, "acos":4, "atan":4, "exp":4, "fact":4} # Dictionary of operator precedence
	binary_left=["+", "-", "*", "/", "%", "C", "P", "L"]
	binary_right=["^"]
	unary_right=["sqrt", "cbrt", "log", "ln", "sin", "cos", "tan", "asin", "acos", "atan", "exp", "fact"]
	
	stack=[] # Operator stack
	postfix=[] # Output list
	
	for i in parsed_list: # Iterate for each character
		
		# Operand found
		if is_float(i): 
			postfix.append(i)
		
		# Opening parenthesis
		elif i=="(": # Opening symbol found
			stack.append(i) # Push opening symbol to stack
		
		# Closing parenthesis
		elif i==")": # Closing symbol found
			while stack and stack[-1]!="(": # Pop until closing symbol found
				postfix.append(stack.pop())
			stack.pop() # Skip opening symbol in output
				
		# Left-associative operators
		elif i in binary_left: # Operator found
			while stack and precedence[stack[-1]]>=precedence[i]: # Left associativity
				postfix.append(stack.pop())
			stack.append(i)
			
		# Right-associative operators
		elif i in binary_right or i in unary_right:
			while stack and precedence[stack[-1]]>precedence[i]: # Right associativity
				postfix.append(stack.pop())
			stack.append(i)
			
		else: # Unknown operator
			raise ValueError("Unknown operator")
			
	while stack: # Pop remaining operators in stack
		postfix.append(stack.pop())
		
	return postfix
