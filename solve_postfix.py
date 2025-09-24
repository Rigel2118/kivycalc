from is_float import is_float
import math

def solve_postfix(postfix, mode="dec", precision=5):

	binary=["+","-","*","/","C","P", "L","%","^"] # List of allowed binary operators
	
	unary=["sqrt", "cbrt", "log", "ln", "sin", "cos", "tan", "asin", "acos", "atan", "exp", "fact"] # List of allowed unary operators
	
	# Solve binary operation
	def binary_operation(a,b,op): 
		try:
			if op in binary: # Check if the operator can be handled
				a,b=float(a),float(b) # Cast operands
				match op: # Pick operations
					case "+": return a+b # Sum case
					case "-": return a-b # Difference case
					case "*": return a*b # Product case
					case "%": return a%b # Modulo case
					case "/": 
						try: return a/b # Quotient case
						except ZeroDivisionError:
							raise ValueError("Division by 0")
					case "^": return a**b # Power case
					case "P": # Permutation case
						a=int(a)
						b=int(b)
						if b > a:
							raise ValueError("r must be < n")
						return math.factorial(a)/math.factorial(a-b)
					case "C": # Combination case
						a=int(a)
						b=int(b)
						if b > a:
							raise ValueError("r must be < n")
						return math.factorial(a)/(math.factorial(b)*math.factorial(a-b))
					case "L": return math.log(b, a) if a != 10 else math.log10(b) 
			else: # Unknown operator
				raise ValueError("Unknown operator")
		except OverflowError:
			raise ValueError("Number too large")
	
	# Solve unary operation
	def unary_operation(a,op): 
		try:
			if op in unary: # Check if the operator can be handled
			
				a=float(a) # Cast operands
				
				match op: # Pick operations
					case "sqrt": return a**(1/2)
					case "cbrt": return a**(1/3)
					case "log": return math.log10(a)
					case "ln": return math.log(a)
					case "sin": 
						if a % math.pi == 0:
							return 0
						return math.sin(a)
					case "cos": 
						if (a-math.pi/2) % (math.pi) == 0:
							return 0
						return math.cos(a)
					case "tan": return math.tan(a)
					case "asin": return math.asin(a)
					case "acos": return math.acos(a)
					case "atan": return math.acos(a)
					case "exp": return math.exp(a)
					case "fact": return math.factorial(int(a))
					
			else: # Unknown operator
				raise ValueError("Unknown operator")
				
		except OverflowError:
			raise ValueError("Number too large")
			
	stack=[] # Stack for saving operands
	
	for i in postfix: # Iterate for each position of the list
	
		if is_float(i): # Operand found
			stack.append(i) # Push to stack
			
		elif i in binary: # Operator found
			operand2=stack.pop() # Second operand is the top element of the stack, then pop
			operand1=stack.pop() # First operand is previous to the top, then pop
			stack.append(binary_operation(operand1,operand2,i)) # Push the result to the stack
			
		elif i in unary: # Operator found
			operand=stack.pop() # Get operand
			stack.append(unary_operation(operand,i)) # Push the result to the stack
	match mode:
		case "dec": result = str(format(float(stack[-1]), ','))
		case "sci": result = str(f"{float(stack[-1]):.{precision}E}")
	print(result)
	if mode == "dec" and '.' in result:
		result = result.rstrip('0').rstrip('.')
	return result # Last element in stack is the answer
