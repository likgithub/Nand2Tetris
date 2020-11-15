import os
#import sys

#Lekhitha Ammaresh

# skip "//", blank spaces, spaces
# a instruction
# c instruction
#this is the one I need to submit (comment for personal checking)
#dictionaries :
comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
    }

dest = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
    }

jump = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
    }


def acommand(aline):
    number = int(aline[1:])
    #print("this is the number", number)
    binary = bin(number)[2:].zfill(16)
    return binary


def ccommand(aline):
    destination = "NA"
    jumps = "NA"
    computation = "NA" #values for debugging purpose
    # dest
    if aline.find("=") != -1:
        dest_mnemonic = aline[0:aline.find("=")]
        for k, v in dest.items():
            if k == dest_mnemonic:
                destination = v
                break

    else:
        destination = "000"

    # jump
    if aline.find(";") != -1:
        jump_mnemonic = aline[aline.find("J"):aline.find("J")+3]
        for k, v in jump.items():
            if k == jump_mnemonic:
                jumps = v
                break

    else:
        jumps = "000"

    #compute
    if aline.find("=") == -1: #comp;jump
        comp_mnemonic = aline[0:aline.find(";")]
    elif aline.find(";") == -1:
        comp_mnemonic = aline[aline.find("=") + 1:] #dest = comp
    else:
        comp_mnemonic = aline[aline.find("=") + 1: aline.find(";")] #dest = comp;jump
        
    temp = comp_mnemonic.split(" ")
    comp_mnemonic = temp[0]
    comp_mnemonic = comp_mnemonic.replace(" ", "")
    comp_mnemonic = comp_mnemonic.replace("\n", "")
    #print("comp mnemonic is", comp_mnemonic)
    for k, v in comp.items():
        #print(k, v, comp_mnemonic, "key, value, comp")
        if k == comp_mnemonic:
            computation = v
            #print("I found the match!")
            break

    return "111" + computation + destination + jumps


symbols = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,

    }
next_free_location = 16    # next available memory location for variables


def cleanline(cline):
    if cline[0] == "/":
        return ""
    elif cline[0] == " ":
        return cleanline(cline[1:])
    else:
        return cline



def lcommand(filename):
    infile = open(filename + ".asm")
    outfile = open(filename + ".tmp", "w")

    line_num = 0
    for lline in infile:
        lline = cleanline(lline)
        if lline == "":
            continue
        elif lline[0] == "(": 
            label = lline[1:lline.find(")")]
            symbols[label] = line_num
            lline = ""
            continue
        elif not lline.strip():
            lline = ""
            continue
        else:
            outfile.write(lline)
            line_num += 1

    infile.close()
    outfile.close()



def tobinary(line):
    global next_free_location
    #print(line)
    if line[0] == "@": #a instruction
        num_or_var = line[1:]
        #print(num_or_var, "is the num_var variable")
        num_or_var = num_or_var.replace(" ", "")
        num_or_var = num_or_var.replace("\n", "")
        #print(num_or_var, "is the num_var variable")
        if num_or_var.isdigit() == False:
            #print("I entered in if false")
            line = symbols.get(num_or_var, -1)
            if line == -1:
                line = "@" + str(next_free_location)
                symbols[num_or_var] = next_free_location
                next_free_location += 1
            else:
                #print("I am in the else - for numbers")
                line = "@" + str(line)

        binaryline = acommand(line)
        return binaryline
    else: #c instruction
        binaryline = ccommand(line)
        return binaryline



#filename = sys.argv[1]
filename = "RectL.asm"
filename = filename[0: len(filename) - 4]

lcommand(filename) #first parse
infile = open(filename + ".tmp")
outfile = open(filename + ".hack", "w")

for line in infile:
    translate_line = tobinary(line)
    #print(translate_line, "<- That is what I am writing to the hack file\n")
    outfile.write(translate_line + "\n")

infile.close()
outfile.close()
os.remove(filename + ".tmp")


