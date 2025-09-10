def parse(string): # Convert plain string into list of numbers and symbols
	size=len(string)
	if size==0:
		raise ValueError("nothing to parse")
	parsed_list=[] # Output
	current="" # String builder
	set1 = set("0123456789.e") # List of allowed numbers
	set2 = set("+-") # Symbols appended to the next number when duplicated
	set3 = set("*/^)%") # Symbols appended to the output when duplicated
	set4 = set("(") # Only allowed to be paired with themselves
	set5 = set("e") # Multipliers
	opened=0 # Counter of opened parentheses
	closed=0 # Counter of closed parentheses
	if string[-1] in set("+-*/^%"):
		raise ValueError("unexpected end of expression")
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
	# Multipliers validity
	if string[0] == "e" or string[-1] == "e":
		raise ValueError("multiplier not valid")
	for j in range(1, size):
		i = j-1
		k = j+1
		if string[j] in set5 and not (string[i] in set1.difference(set(".e")) and string[k] in set1.difference(set(".e")).union(set2)):
			raise ValueError("multiplier not valid")
			
	i=0 # Initialize counter
	
	while i<size: # Loop until true
		if string[i] in set1: # Is a number
			if parsed_list and parsed_list[-1]==")": # There can't be a number after a closing parenthesis
				raise ValueError("unexpected number")
			points=0 # Counter of decimal points inside a number
			signs=0
			minus=0
			multiplier_mode = False
			while i<size and string[i] in set1: # Build first element
				if string[i] == "e":
					multiplier_mode = True
					current+=string[i] # Push to string
					i+=1 # Next position
					break
				if string[i]==".": # Account for decimals
					points+=1
				if points>1: # Only one decimal place is allowed
					raise ValueError("too many decimals")
				current+=string[i] # Push to string
				i+=1 # Next position
			while multiplier_mode and i<size and string[i] in set1.union(set2):
				
				# Exponent
				if string[i] in set1: # Number encountered
					while i<size and string[i] in set1:
						if string[i]==".": # Account for decimals
							raise ValueError("multiplier cannot have decimals")
						if string[i]=="e": # Repeated multiplier
							raise ValueError("multiplier not valid")
						current += string[i]
						i+=1
					break
							
				# Sign of the exponent
				elif string[i] in set2: # Sign encountered
					while i<size and string[i] in set2:
						if string[i]==".": # Account for decimals
							raise ValueError("multiplier cannot have decimals")
						if string[i]=="e": # Repeated multiplier
							raise ValueError("multiplier not valid")
						if string[i] == "-":
							minus+=1
						i+=1
					if minus%2 != 0:
						current += "-"
					
				# Output: current must be correct, ready to append
			zeros=True # Helper
			for j in current: # Check if the built number is made of zeros
				if j not in set("0."):
					zeros=False
			if zeros and parsed_list and parsed_list[-1]=="/": # Division by zero case
				raise ValueError("division by 0")
			if i==size and string[-1]==".": # Last character is a decimal
				raise ValueError("missing decimal side")
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

			if not parsed_list or parsed_list[-1] in set("*/^(%"): # Sign is treated as part of the next number
				if sign=="-": # Plus sign is not necessary
					current+=sign # Append to the number builder
			else: # Sign is treated as an operator
				parsed_list+=[sign] # Append to output
		elif string[i] in set3: # Symbol is in set 3
			if not parsed_list or parsed_list[-1] in set("+-*/^(%"): # These can't be at the start of expression or after the named operators
				raise ValueError("unexpected symbol")
			parsed_list+=[string[i]] # Append to output
			i+=1
		elif string[i] in set4: # Opened parenthesis
			if parsed_list and parsed_list[-1] not in set("+-*/^(%"): # Can't be after a number or a closed parenthesis
				raise ValueError("unexpected symbol")
			parsed_list+=[string[i]] # Append to output
			i+=1
	return parsed_list
