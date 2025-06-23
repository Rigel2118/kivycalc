def parse(string): # Convert plain string into list of numbers and symbols
	size=len(string)
	if size==0:
		raise ValueError("nothing to parse")
	parsed_list=[] # Output
	current="" # String builder
	set1 = set("0123456789.") # List of allowed numbers
	set2 = set("+-") # Symbols appended to the next number when duplicated
	set3 = set("*/^)") # Symbols appended to the output when duplicated
	set4 = set("(") # Only allowed to be paired with themselves
	opened=0 # Counter of opened parentheses
	closed=0 # Counter of closed parentheses
	for i in string: # Congruence of parentheses
		if i=="(":
			opened+=1 # Account for opened parentheses
		elif i==")":
			closed+=1 # Account for closed parentheses
			if closed>opened:
				raise ValueError("unmatched parentheses")
	if not opened==closed:
		raise ValueError("unmatched parentheses")
	flag=False
	for i in string: # Check for existence of numbers
		if i in set1:
			flag=True
			break
	if not flag:
		raise ValueError("no numbers detected")
	i=0 # Initialize counter
	while i<size: # Loop until true
		if string[i] in set1: # Is a number
			if parsed_list and parsed_list[-1]==")": # There can't be a number after a closing parenthesis
				raise ValueError("unexpected number")
			points=0 # Counter of decimal points inside a number
			while i<size and string[i] in set1: # Build first element
				if string[i]==".": # Account for decimals
					points+=1
				if points>1: # Only one decimal place is allowed
					raise ValueError("decimal place overflow")
				current+=string[i] # Push to string
				i+=1 # Next position
			if i==size and string[-1]==".": # Last character is a decimal
				raise ValueError("missing decimal part")
			parsed_list+=[current] # Once it's built, push to output
			current="" # Reset builder
		elif string[i] in set2: # Account for signs
			minus=0 # Counter of minus signs encountered
			while i<size and string[i] in set2: # Run through every sign
				if string[i]=="-":
					minus+=1
				i+=1
			if i==size: # Reached end of expression and no number is found
				raise ValueError("unexpected end of expression")
			if string[i] not in set1.union("("): # Found unexpected operator operator
				raise ValueError("unexpected operator")
			sign="" # Helper
			if minus%2==0: # Even minus
				sign="+"
			else: # Odd minus
				sign="-"
			if not parsed_list or parsed_list[-1] in set("*/^("): # Sign is treated as part of the next number
				if sign=="-": # Plus sign is not necessary
					current+=sign # Append to the number builder
			else: # Sign is treated as an operator
				parsed_list+=[sign] # Append to output
		elif string[i] in set3: # Symbol is in set 3
			if not parsed_list or parsed_list[-1] in set("+-*/^("): # These can't be at the start of expression or after the named operators
				raise ValueError("unexpected symbol")
			parsed_list+=[string[i]] # Append to output
			i+=1
		elif string[i] in set4: # Opened parenthesis
			if parsed_list and parsed_list[-1] not in set("+-*/^("): # Can't be after a number or a closed parenthesis
				raise ValueError("unexpected symbol")
			parsed_list+=[string[i]] # Append to output
			i+=1
	return parsed_list
