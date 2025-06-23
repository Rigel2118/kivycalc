from is_float import is_float
def infix_to_postfix(parsed_list):
    precedence={"(":0,"+":1,"-":1,"*":2,"/":2,"^":3} # Dictionary of operator precedence
    stack=[] # Operator stack
    postfix=[] # Output list
    for i in parsed_list: # Iterate for each character
        if is_float(i): # Operand found
            postfix.append(i)
        elif i=="(": # Opening symbol found
            stack.append(i) # Push opening symbol to stack
        elif i==")": # Closing symbol found
            while stack and stack[-1]!="(": # Pop until closing symbol found
                postfix.append(stack.pop())
            stack.pop() # Skip opening symbol in output
        elif i in precedence: # Operator found
            if i=="^": # Case of powers
                while stack and precedence[stack[-1]]>precedence[i]: # Right associativity
                    postfix.append(stack.pop())
            else: # Case of +,-,*,/
                while stack and precedence[stack[-1]]>=precedence[i]: # Left associativity
                    postfix.append(stack.pop())
            stack.append(i)
        else: # Unknown operator
            raise ValueError("Unknown operator")
    while stack: # Pop remaining operators in stack
        postfix.append(stack.pop())
    return postfix
