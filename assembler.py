# ----------------------------------------
# FILENAME: assembler.py
# AUTHOR: Raúl Montoliu
# LAST MODIFICATION: 23/11/2021
# ----------------------------------------
# Obtain the hack machine code from a hack assembly program
# RUN: python assembler.py asm_filename hack_filename
# ----------------------------------------
# NOTE: If a bug is detected, please send a report to montoliu@uji.es
# ----------------------------------------
from sys import argv


# ----------------------------------------
# Read a file from disk
# The output is a list of strings, 
#   each string is a line of the program
# ----------------------------------------
def read_file(filename):
    code = []
    with open(filename, 'r') as filehandle:
        for line in filehandle:
            line = line[:-1]
            code.append(line)
    return code


# -------------------------------------------
# write a program (list of strings) to disk
# -------------------------------------------
def write_file(code, filename):
    with open(filename, 'w') as filehandle:
        for listitem in code:
            filehandle.write('%s\n' % listitem)


# -------------------------------------------------------------------------------
# Get the "a" and "c's" bits of the instruction given the computation
# In case of given an illegal computation, return -1 and print an error message
# -------------------------------------------------------------------------------
def get_computation(computation):
    if computation == "0":
        return "0101010"
    elif computation == "1":
        return "0111111"
    elif computation == "-1":
        return "0111010"
    elif computation == "D":
        return "0001100"
    elif computation == "A":
        return "0110000"
    elif computation == "!D":
        return "0001101"
    elif computation == "!A":
        return "0110001"
    elif computation == "-D":
        return "0001111"
    elif computation == "-A":
        return "0110011"
    elif computation == "D+1":
        return "0011111"
    elif computation == "A+1":
        return "0110111"
    elif computation == "D-1":
        return "0001110"
    elif computation == "A-1":
        return "0110010"
    elif computation == "D+A":
        return "0000010"
    elif computation == "D-A":
        return "0010011"
    elif computation == "A-D":
        return "0000111"
    elif computation == "D&A":
        return "0000000"
    elif computation == "D|A":
        return "0010101"
    elif computation == "M":
        return "1110000"
    elif computation == "!M":
        return "1110001"
    elif computation == "-M":
        return "1110011"
    elif computation == "M+1":
        return "1110111"
    elif computation == "M-1":
        return "1110010"
    elif computation == "D+M":
        return "1000010"
    elif computation == "D-M":
        return "1010011"
    elif computation == "M-D":
        return "1000111"
    elif computation == "D&M":
        return "1000000"
    elif computation == "D|M":
        return "1010101"
    else:
        print("Bad computation " + computation)
        return "-1"


# -------------------------------------------------------------------------------
# Get the "d's" bits of the instruction given the destination
# In case of given an illegal destination, return -1 and print an error message
# -------------------------------------------------------------------------------
def get_destination(destination):
    if destination == "":
        return "000"
    elif destination == "M":
        return "001"
    elif destination == "D":
        return "010"
    elif destination == "MD":
        return "011"
    elif destination == "A":
        return "100"
    elif destination == "AM":
        return "101"
    elif destination == "AD":
        return "110"
    elif destination == "AMD":
        return "111"
    else:
        print("Bad destination " + destination)
        return "-1"


# -------------------------------------------------------------------------
# Get the "j's" bits of the instruction given the jump
# In case of given an illegal jump, return -1 and print an error message
# -------------------------------------------------------------------------
def get_jump(jump):
    if jump == "":
        return "000"
    elif jump == "JGT":
        return "001"
    elif jump == "JEQ":
        return "010"
    elif jump == "JGE":
        return "011"
    elif jump == "JLT":
        return "100"
    elif jump == "JNE":
        return "101"
    elif jump == "JLE":
        return "110"
    elif jump == "JMP":
        return "111"
    else:
        print("Bad jump " + jump)
        return "-1"


# ---------------------------------------------------
# given a C instruction, get the three parts.
# If a part is not present, returns "" for this part
# ---------------------------------------------------
def get_instruction_parts(asm_line):
    # jump is the part after ";" (if it exists)
    idx_jmp = asm_line.find(";")
    if idx_jmp == -1:
        str_jump = ""
    else:
        str_jump = asm_line[idx_jmp + 1:]

    # destination is the part before "=" (if it exists)
    idx_dest = asm_line.find("=")
    if idx_dest == -1:
        str_destination = ""
    else:
        str_destination = asm_line[:idx_dest]

    # computation is the part after "=" and before ";""
    if idx_jmp != -1 and idx_dest != -1:
        str_computation = asm_line[idx_dest+1:idx_jmp]
    elif idx_jmp != -1 and idx_dest == -1:
        str_computation = asm_line[:idx_jmp]
    elif idx_jmp == -1 and idx_dest != -1:
        str_computation = asm_line[idx_dest + 1:]
    else: # both == -1
        str_computation = asm_line

    return str_destination, str_computation, str_jump


# -------------------------------------------------
# Get bits of the instruction if it is of type C
# If any error, returns "----------------"
# -------------------------------------------------
def instructionC(asm_line):
    str_destination, str_computation, str_jump = get_instruction_parts(asm_line)
    bin_destination = get_destination(str_destination)
    bin_computation = get_computation(str_computation)
    bin_jump = get_jump(str_jump)

    if bin_destination != -1 and bin_computation != -1 and bin_jump != 1:
        return "111" + bin_computation + bin_destination + bin_jump
    else:
        return "----------------"


# -----------------------------------------------
# Get bits of the instruction if it is of type A
# If any error, returns "----------------"
# -----------------------------------------------
def instructionA(asm_line):
    str_num = asm_line[1:]
    dec_num = int(str_num)

    # Maxim positive number is 16383, and minimum negative number is -16384
    if dec_num > 16383 or dec_num < -16384:
        print("Number " + str(dec_num) + " is out of range to be represented using 15 bits")
        return "----------------"

    if dec_num >= 0:
        str_bin = str(bin(dec_num))[2:].zfill(15)     # Fill with 0's to the left
    else:
        str_bin = str(bin((1 << 15) + dec_num))[2:]   # For negative numbers

    return "0" + str_bin


# ----------------------------------------
# Do the compilation line by line
# The assembly code must be preprocessed
# ----------------------------------------
def assembler(asm):
    hack_code = []

    for asm_line in asm:
        if asm_line[0] == '@':
            hack_line = instructionA(asm_line)
        else:
            hack_line = instructionC(asm_line)

        hack_code.append(hack_line)
    return hack_code


# ----------------------------------------
# Delete spaces and empty lines from code
# ----------------------------------------
def delete_spaces_and_empty_lines(asm_code):
    new_asm_code = []
    for line in asm_code:
        new_line = line.replace(" ", "")
        new_line2 = new_line.replace("\t", "")
        if len(new_line2) > 0:
            new_asm_code.append(new_line2)
    return new_asm_code


# -----------------------------------------------------------
# Delete comments. Comments starts with "/"
# They can be at the beginning of the line or after the code
# -----------------------------------------------------------
def delete_comments(asm_code):
    new_asm_code = []
    for line in asm_code:
        idx = line.find("/")
        if idx == -1:
            new_asm_code.append(line[:])
        else:
            if idx != 0:
                new_line = line[:idx]
                new_asm_code.append(new_line)

    return new_asm_code

# ----------------------------------------------------------
# Deal with (LABEL)
# Replace @LABEL with the corresponding number of code line
# ----------------------------------------------------------
def deal_with_labels(asm_code):
    labels = {}  # key: label, value: line number

    # Fill labels dictionary
    line_number = 0
    for line in asm_code:
        if line[0] == "(":
            label = line[1:len(line)-1]
            labels[label] = line_number
        else:
            line_number += 1

    # Replace labels by line numbers
    # Delete labels lines
    new_asm_code = []
    for line in asm_code:
        if line[0] != "(":
            if line[0] == "@":
                label = line[1:]
                if label.lstrip("-").isnumeric():
                    new_asm_code.append(line)
                elif label in labels:
                    value = labels[label]
                    new_asm_code.append("@" + str(value))
                else:
                    new_asm_code.append(line[:])
            else:
                new_asm_code.append(line[:])

    return new_asm_code

# ----------------------------------------------------------
# Replace variables with the corresponding RAM position
# ----------------------------------------------------------
def deal_with_variables(asm_code):
    variables = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4, "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4,
                 "R5": 5, "R6": 6, "R7": 7, "R8": 8, "R9": 9, "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14,
                 "R15": 15, "SCREEN": 16384, "KBD": 24576}

    # look for variables
    ram = 16
    for line in asm_code:
        if line[0] == "@":
            label = line[1:len(line)]
            if not label.lstrip("-").isnumeric() and label not in variables:
                variables[label] = ram
                ram += 1

    # replace variables for ram positions
    new_asm_code = []
    for line in asm_code:
        if line[0] == "@":
            label = line[1:len(line)]
            if label in variables:
                new_asm_code.append("@" + str(variables[label]))
            else:
                new_asm_code.append(line[:])
        else:
            new_asm_code.append(line[:])

    return new_asm_code


# ----------------------------------------
# 1. Delete all spaces and empty lines
# 3. Delete comments
# 4. Deal with line code labels
# 5. Deal with variable names
# ----------------------------------------
def preprocess(asm_code):
    new_asm_code = delete_spaces_and_empty_lines(asm_code)
    new_asm_code = delete_comments(new_asm_code)
    new_asm_code = deal_with_labels(new_asm_code)
    new_asm_code = deal_with_variables(new_asm_code)

    return new_asm_code


# -----------------------------------------------
# -                    MAIN                     -
# -----------------------------------------------
# Use: python assembler.py input.asm output.hack
# -----------------------------------------------
if __name__ == "__main__":
    asm_filename = argv[1]
    hack_filename = argv[2]

    print("Assembling " + asm_filename + " to " + hack_filename)

    asm_code = read_file(asm_filename)     # read asm code from disk
    asm_code = preprocess(asm_code)        # preprocess code
    hack_code = assembler(asm_code)        # asm -> hack
    write_file(hack_code, hack_filename)   # write hack code to disk
