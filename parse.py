import string as strlib
import math

def parse(string, ANS): # Convert plain string into list of numbers and symbols
	
	# Null string case
	if len(string)==0:
		raise ValueError("nothing to parse")
	parsed_list=[] # Output
	current="" # String builder
	
	# Pre-made sets
	set1 = set("0123456789.eπE") # List of allowed numbers
	set2 = set("+-") # Symbols appended to the next number when duplicated
	set3 = set("*/^)%CPL") # Symbols appended to the output when duplicated
	set4 = set("(") # Only allowed to be paired with themselves
	set5 = set("E") # Multipliers
	
	# Special functions -> we use "o" as a escape character
	set6 = {"sqrt", "cbrt", "log", "ln", "sin", "cos", "tan", "asin", "acos", "atan", "exp", "fact", "comb", "perm"} 
	
	
	opened=0 # Counter of opened parentheses
	closed=0 # Counter of closed parentheses
	
	# Remove spaces
	string = string.replace(" ", "")
	
	# Obviously wrong cases
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
	
	# Replace ANS
	if string.find("ANS") != -1:
		# Check emptiness
		if ANS == "":
			raise ValueError("no previous ANS")
			
		# Format string
		ANS = ANS.replace(",", "").strip()
		
		i=0
		while i < len(string):
			j = string.find("ANS", i)
			if j != -1:
				if j > 0 and j < len(string)-3 and (string[j-1] in set1 or string[j+3] in set1):
					raise ValueError("misplaced ANS")
				i = j+3
			else:
				break
		string = string.replace("ANS", ANS)
		
	# Check for existence of numbers
	for i in string: 
		if i in set1:
			flag=True
			break
	if not flag:
		raise ValueError("no numbers detected")
	
	# Multipliers validity
	if string[0] == "E" or string[-1] == "E":
		raise ValueError("multiplier not valid")
	for j in range(1, len(string)):
		i = j-1
		k = j+1
		if string[j] in set5 and not (string[i] in set1.difference(set(".E")) and string[k] in set1.difference(set(".E")).union(set2)):
			raise ValueError("multiplier not valid")
	
	# Replace constants
	i=0
	while i < len(string):
		if string[i] in {"e", "π"}:
			if i == 0 and string[i+1] in set("0123456789."):
				raise ValueError("constant not valid")
			elif i == len(string)-1 and string[i-1] in set("0123456789."):
				raise ValueError("constant not valid")
			elif i > 0 and i < len(string)-1 and (string[i-1] in set("0123456789.") or string[i+1] in set("0123456789.")):
				raise ValueError("constant not valid")
			if i == 0 and string[i+1] in strlib.ascii_lowercase:
				i+=1
				continue
			elif i == len(string)-1 and string[i-1] in strlib.ascii_lowercase:
				i+=1
				continue
			
			elif i > 0 and i < len(string)-1 and (string[i-1] in strlib.ascii_lowercase or string[i+1] in strlib.ascii_lowercase):
				i+=1
				continue
			match string[i]:
				case "e": string = string[:i]+"{math.e}"+string[i+1:]
				case "π": string = string[:i]+f"{math.pi}"+string[i+1:]
		i+=1
	# 3.141592653589793
	# 2.718281828459045
	
	print(string)
	# Convert factorial symbol to unary function
	i=0
	while i < len(string):
		if string[i] == "!":
			string = string[:i]+string[i+1:]
			if string[i-1] == ")":
				j=i-1
				while string[j] != "(":
					j-=1
				string = string[:j]+"fact"+string[j:]
			elif string[i-1] in set1:
				j=i-1
				while string[j] not in set1:
					j-=1
				string = string[:j]+"fact"+"("+string[j:i]+")"+string[i:]
			else:
				raise ValueError("factorial not valid")
		i+=1
	
	# Rewrite logarithms
	i=0
	while i < len(string):
		j = string.find("log", i)
		if j != -1:
			if j != -1:
				if string[j+3] != "(":
					raise ValueError("missing parenthesis")
			if j>0 and (string[j-1] in set1 or string[j-1] == ")"): # Binary logarithm
				string = string[:j] + "L" + string[j+3:] # Becomes one-character
				print(string)
			i = j+1
		else:
			break
		
	# Special operators (unary)
	for i in set6:
		j=0
		while j < len(string):
			k = string.find(i,j)
			if k != -1: # Found
				if k == 0 or (string[k-1] in set("+-*/^(") and string[k+len(i)] == "("): # Check if it's a whole word
					string = string[:k] + "o" + string[k:]
					j = k+1+len(i)
				else:
					j = k+len(i)
			else: 
				break
			
			
	# Main parsing loop for binary operators
	i=0 # Initialize counter
	while i<len(string): 
		
		# Is a number
		if string[i] in set1: 
		
			if parsed_list and parsed_list[-1]==")": # There can't be a number after a closing parenthesis
				raise ValueError("unexpected number")
				
			points=0 # Counter of decimal points inside a number
			signs=0
			minus=0
			multiplier_mode = False
			
			while i<len(string) and string[i] in set1: # Build first element
			
				if string[i] == "E":
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
				
			while multiplier_mode and i<len(string) and string[i] in set1.union(set2):
				
				# Exponent
				if string[i] in set1: # Number encountered
					while i<len(string) and string[i] in set1:
						if string[i]==".": # Account for decimals
							raise ValueError("multiplier cannot have decimals")
						if string[i]=="eπE": # Repeated multiplier
							raise ValueError("multiplier not valid")
						current += string[i]
						i+=1
					break
							
				# Sign of the exponent
				elif string[i] in set2: # Sign encountered
					while i<len(string) and string[i] in set2:
						if string[i]==".": # Account for decimals
							raise ValueError("multiplier cannot have decimals")
						if string[i]=="eπE": # Repeated multiplier
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
			if i==len(string) and string[-1]==".": # Last character is a decimal
				raise ValueError("missing decimal side")
			parsed_list+=[current] # Once it's built, push to output
			current="" # Reset builder
		
		# Account for signs
		elif string[i] in set2: 
			minus=0 # Counter of minus signs encountered
			
			while i<len(string) and string[i] in set2: # Run through every sign
				if string[i]=="-":
					minus+=1
				i+=1
			
			if i==len(string): # Reached end of expression and no number is found
				raise ValueError("unexpected end of expression")
			
			if string[i] not in set1.union("(o"): # Found unexpected operator operator
				raise ValueError("unexpected operator")
			
			sign="" # Helper
			if minus%2==0: # Even minus
				sign="+"
			else: # Odd minus
				sign="-"

			if not parsed_list or parsed_list[-1] in set("*/^(%CPL"): # Sign is treated as part of the next number
				if sign=="-": # Plus sign is not necessary
					current+=sign # Append to the number builder
			else: # Sign is treated as an operator
				parsed_list+=[sign] # Append to output
				
		# Symbol is in set 3
		elif string[i] in set3: 
			if not parsed_list or parsed_list[-1] in set("+-*/^(%CPL"): # These can't be at the start of expression or after the named operators
				raise ValueError("unexpected symbol")
			parsed_list+=[string[i]] # Append to output
			i+=1
			
		# Opened parenthesis
		elif string[i] in set4: 
			if parsed_list and parsed_list[-1] not in set("+-*/^(%oCPL") : # Can't be after a number or a closed parenthesis
				raise ValueError("unexpected symbol")
			parsed_list+=[string[i]] # Append to output
			i+=1
		
		# Special symbols case
		elif string[i] == "o": # Escape character found
			if string[i-1] in set1.union(set5):
				raise ValueError("number before s. operator")
			
			j = i+1
			op = ""
			while string[j] != "(":
				op += string[j]
				j+=1
			
			if op not in set6: # Operator validity
				raise ValueError("unknown operator")
			if string[j+1] == ")":
				raise ValueError("empty s. operator")
			parsed_list+=[op,"("]
			i=j+1
	print(parsed_list)
	return parsed_list
