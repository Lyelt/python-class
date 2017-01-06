#Expression Evaluator w/ Binary
#Nicholas Ghobrial Program 1 Assignment
cont = True
while (cont):
    expression = input("Please enter the calculation to perform in binary: ")
    sub = False #For checking negative subtraction value
    index = 0
    while expression[index] != "+" and expression[index] != "-" and expression[index] != "*" and expression[index] != "/":
        index += 1
    
    #Determine which operator was entered and each string to be evaluated
    operator = expression[index]
    binaryString1 = expression[:index]
    binaryString2 = expression[index+1:]
    
    #Assuming user is entering spaces in their input, this ignores them
    binaryLen1 = len(binaryString1) - 1
    binaryLen2 = len(binaryString2) - 1
    
    number1 = number2 = 0
    
    for i in range(0, binaryLen1):      #Walk through the first binary number
        n = binaryLen1 - i - 1          #Raise 2 to a power based on where the 1 is present   
        if (binaryString1[i] == "1"):
            number1 += 2**n             #Add the number if there is a 1. Ignore if there is a 0

    for i in range(0, binaryLen2+1):    
        n = binaryLen2 - i
        if (binaryString2[i] == "1"):
            number2 += 2**n
            
    #Examine operator and perform corresponding operation
    if (operator == "+"):
        result = number1 + number2
    elif (operator == "-"):
        #Check if subtracting a larger number from a smaller number
        if number2 > number1:
            number1, number2 = number2, number1 #Swap and flip the sign
            sub = True
        result = number1 - number2
    elif (operator == "*"):
        result = number1 * number2
    elif (operator == "/"):
        if number2 == 0:    #Check for zero denominator
            print("Cannot divide by zero")
        else:
            result = number1 / number2
    else:
        print("Operator could not be determined")
    
    if result > 65025:
    #Error if user tries to input larger than 11111111 * 11111111
        print ("Input too large.")
    else:
    #Convert answer back into binary
        binaryResult = " "
        while result > 0:
            r = result % 2
            #Add a 0 or 1 based on remainder of result / 2
            if (r == 0):
                binaryResult = "0" + binaryResult
            elif (r == 1):
                binaryResult = "1" + binaryResult
            result = result // 2 #Round down for next calculation
        if sub:
            binaryResult = "-" + binaryResult     #Adjust if we subtracted a larger number
        
        #Echo the input and show result
        print(binaryString1 + operator + binaryString2 + " = " + binaryResult)
    
    #Continue calculating?
    while True:
        prompt = input("Would you like to continue? (Y/N) ")
        if prompt.upper() == "N":
            cont = False
            print ("Thank you for using this binary calculator!")
            break
        elif prompt.upper() == "Y":
            cont = True
            break
        else:
            print("Invalid response.")