import sys
import os
def main():
    with open("examples.txt", "r") as ins: # reads text file for the lexical analyzer
        array = [] #creating a list to append the lines of examples.txt into
        for line in ins:
            array.append(line.rstrip()) #strip the trailing new line characters
    for exp in array: #craetes an array of strings
        x = tokenizer(exp.rstrip()) #remove trailing new line character
        recognizer(exp,x)
class builder:
    other = ["abcdefghijklmnopqrstuvwxyz", "0123456789", "+-/*", "=", " "]
    stateArray = []
    with open("states.txt", 'r') as f:  # Reads the state table text file which is strings of numbers
        for line in f.readlines(): #read lines as strings
            stateArray.append(line.rstrip().split(' ')) #split the lines with spaces and remove trailing new line character
    states = ["start","identifier","number","operator","assignment","error"] #states which are in order and are represented by their respective index
def tokenizer(str2):
    """This function takes a string and then tokenizes it and returns the names of the tokens which are the states"""
    currentState = 0 #0 is the starting state
    finalString = "" #this is the string that will be concatanated to and then returned
    tempString = ""
    k = 0 #variable used for iterating
    while k < len(str2):
        char2 = str2[k] #using index to assign a character
        nextState = getNewState(char2,currentState) #getting the next state
        if (currentState != nextState): #if the state has changed that then means a token just ended
            oldState = currentState #swapping the old state and the new state
            currentState = nextState #swapping the current state and the next state
            if len(tempString) > 0:
                finalString += (builder.states[int(oldState)] + ":" + tempString + " ")
            tempString = ""
        if currentState != 0: # if the current state does not equal 0 and the character is not a space then concatenate it with the tempString
            if char2 != " ": #this is a check to skip over the spaces in the string
                tempString += char2
        if (k == (len(str2) -1) and len(tempString) > 0):
            finalString += builder.states[int(currentState)] + ":" + tempString
        k +=1
    return str(finalString)
def getNewState(character, currentState):
    """Function that is passed 2 parameters
    characer = a single string character
    currentState = the current state that we are at in the string
    returns a integer which represents the state"""
    for item in builder.other: #This is an efficient iteration method for going through all the possible characters that could represent
                                # every state except 5 (error)
        if (item.find(character)) != -1: #the find method returns a -1 if the character is not found
            return builder.stateArray[int(currentState)][builder.other.index(item)] #if the character is found then a new state is returned
    return builder.stateArray[int(currentState)][len(builder.stateArray)-1] #if the character is not found then return the error state
def recognizer(exp, stringy):
    """This method takes 2 parameters
    exp = this is the original string which is a result of reading the text file, this is used for printing purposes
    stringy = a string which is the result of the tokenizer function
    this function does not return anything but instead prints the needed string
    """
    grammar = [["assign_stmt", "expression", "identifier assignment expression", "identifier operator expression",
             "number operator expression", "identifier", "number"],
    ["statement", "statement", "assign_stmt", "expression", "expression", "expression", "expression"]]
    #This 2d array is used to represent the grammar for the recognizer
    k = 0
    recString = "" #string where only the token names are added to it as a result of stripping everything else from stringy
    stateNames = []
    switch = True #boolean trigger
    while k < len(stringy):
        char2 = stringy[k] #using the index in stringy to assign a character to a variable
        if (char2 == ":"): #if a colon is found we do not want that added to the statenames
            stateNames.append(str(recString)) #stateNames will contain only strings found in the states list
            recString = ""
            switch = False;
        if switch:
            recString += char2
        if (char2 == " "): #if a space is found then concatenating to the recString needs to starts again
            switch = True
        k += 1
    newNames = stateNames #the final string of statenames is assigned to a new variable
    index = 0
    while index < len(newNames):
        i = 0
        current = stringer(newNames, index) #function call to the stringer function passing a string list
        same = False
        while i < len(grammar[0]):
            if  (grammar[0][i] == current):
                newNames = newNames[0:index]
                newNames.append(grammar[1][i]) #appending to the list using a similar method as the tokenizer to select the right index
                same = True
                break
            i+=1
        if (not same):
            index += 1
        else:
            index = 0
        if(newNames[0] == "statement"):
            print(exp + " tokenizes as " + (" ".join(stateNames))) #printing the original expression as well as a string and joining the stateNames list
            print("         " + exp + " is a valid statement") #if the stringy made it this far then it is a valid statement
            return
    print(exp + " tokenizes as " + (" ".join(stateNames)))
    print("         " + exp + " is an Invalid statement") #if the stringy made it to here then it is not a valid statement
    return
def stringer(tokens, index):
    """This function takes 2 parameters
    tokens = a list of strings
    index = an int
    and returns the list of strings with spaces inbetween them"""
    stringy = ""
    i = index
    while i  < len(tokens):
        stringy += tokens[i]
        if (i < len(tokens)-1):
            stringy += " "
        i+=1
    return stringy
main()