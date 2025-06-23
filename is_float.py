def is_float(string): # Check if a string is a number
	try:
		float(string) # Try cast to float
		return True
	except ValueError: # Catch the error
		return False
