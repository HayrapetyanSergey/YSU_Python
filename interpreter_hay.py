import sys

variable_dict = {}
list_of_text = []

if not sys.argv[1].endswith(".hay"):
    raise FileNotFoundError("File must have .hay extension")

with open(sys.argv[1], "r") as f:
    list_of_lines = [line.strip() for line in f.readlines()]

    for line in list_of_lines:
        if line != "":
            list_of_text.append(line)



def is_syntax_right(txt):
    """This Function is cheking count of 'if', 'while', 'for' and '!'. They must be equal:"""

    counter = 0
    for line in txt:
        if "if" in line:
            counter += 1
        if "while" in line:
            counter += 1
        if "for" in line:
            counter += 1
        elif "!" in line:
            counter -= 1

    if counter != 0:
        raise SyntaxError("Number of 'if, while,for' and '!' must be equal:")


def printing(txt, idx):
    """This Function performs the printing process and checks the syntax"""

    if "print" in txt[idx] and 0 <= len(txt):
        row = ' '.join(list(txt[idx]))
        if row[5] != "[" and row[-1] != "]":
            raise SyntaxError("After print you must start with '[' and finish with']'")

        row = (list_of_text[idx].split("print["))[1].split("]")[0].split(" ")

        for ind in range(len(row)):
            if row[ind] in variable_dict:
                row[ind] = str(variable_dict[row[ind]])
        try:
            print(eval(' '.join(row)))
        except:
            print(" ".join(row))


def variable_after_declaring(idx):
    """A function that performs the following assignment operations"""

    arg = list_of_text[idx].split()
    if arg[0] in variable_dict and arg[1] == ":=":
        for i in range(2, len(arg)):
            if arg[i] in variable_dict:
                arg[i] = str(variable_dict[arg[i]])
        variable_dict[arg[0]] = eval(" ".join(arg[2:]))


def already_declared(idx):
    """This function is cheking, that declared variables were been declared. """

    row = list_of_text[idx].split()
    if row[1] in variable_dict:
        row[1] = variable_dict[row[1]]


def creating_variable(arg):
    """This function assign value in variable."""

    for i in range(3, len(arg)):
        if arg[i] in variable_dict:
            arg[i] = str(variable_dict[arg[i]])
    variable_dict[arg[1]] = eval(" ".join(arg[3:]))


def variable_name(row):
    """This function is cheking or does it start with ascii letter?"""

    if not row[1][0].isalpha():
        raise SyntaxError("Variables must start with ascii letter.")


def variable_value(row):
    """This function is assigns values"""
    
    for i in range(len(row)):
        if row[i] in variable_dict:
            row[i] = str(variable_dict[row[i]])


def is_declared(idx):
    """This function ceking Is the variable declared?"""

    row = list_of_text[idx].split()
    for i in range(5):
        if row[0] in variable_dict or ["if", "while", "print", "var", "!"][i] in row[0]:
            return True

    raise NameError(f"Name ({str(row[0])})' is unrecognizable.")


def untill_if_while_for(ind = 0):
    """This function do file line by line untill will reach a line that starts with 'if'"""

    while ind != len(list_of_text):
        if "if" in list_of_text[ind] or "while" in list_of_text[ind] \
                or "for" in list_of_text[ind]:
            break

        splitted_row = list_of_text[ind].split()

        if "var" in list_of_text[ind]:
            variable_name(splitted_row)
            already_declared(ind)
            creating_variable(splitted_row)

        variable_after_declaring(ind)
        is_declared(ind)
        printing(list_of_text, ind)

        ind += 1


def after_if(idx):
    """This function is checking, or does it  ends with '!'"""

    if "!" not in list_of_text[idx:]:
        raise SyntaxError("After if you mast end with !")


def have_if():
    """This function do file line by line when reach a line that starts 'if'
    and will do untill will reach line that ends with '!''"""

    ind = 0

    while ind != len(list_of_text):
        if "if" in list_of_text[ind]:
            splitted_row = list_of_text[ind].split()
            after_if(ind)
            variable_value(splitted_row)

            if eval(' '.join(splitted_row[1:])):
                while list_of_text[ind] != "!":
                    if "var" in list_of_text[ind]:
                        splitted_row = list_of_text[ind].split()
                        variable_name(splitted_row)
                        already_declared(ind)
                        creating_variable(splitted_row)

                    variable_after_declaring(ind)
                    is_declared(ind)
                    printing(list_of_text, ind)

                    ind += 1

                if ind != len(list_of_text):
                    untill_if_while_for(ind)

            else:
                while "!" not in list_of_text[ind]:
                    ind += 1
                untill_if_while_for(ind)
        ind += 1


def after_while(idx):
    """This function is checking, or does While ends with '!'"""

    if "!" not in list_of_text[idx:]:
        raise SyntaxError("After While you mast end with !")


def have_while():
    """This function do file line by line when reach a line that starts 'while'
    and will do untill will reach line that ends with '!''"""

    ind = 0

    while ind != len(list_of_text):
        if "while" in list_of_text[ind]:
            splitted_row = list_of_text[ind].split()
            after_while(ind)
            variable_value(splitted_row)

            if eval(' '.join(splitted_row[1:])):
                while list_of_text[ind] != "!":
                    if "var" in list_of_text[ind]:
                        splitted_row = list_of_text[ind].split()
                        variable_name(splitted_row)
                        already_declared(ind)
                        creating_variable(splitted_row)

                    variable_after_declaring(ind)
                    is_declared(ind)
                    printing(list_of_text, ind)

                    ind += 1

                if ind != len(list_of_text):
                    untill_if_while_for(ind)

            else:
                while "!" not in list_of_text[ind]:
                    ind += 1
                untill_if_while_for(ind)

        ind += 1


def do_while():
    """This function does while loop"""

    for ind in range(len(list_of_text)):
        if 'while' in list_of_text[ind]:
            splitted_row = list_of_text[ind].split()
            while variable_dict[splitted_row[1]] < int(splitted_row[-1]):
                have_while()


def is_syntax_right_from_to(txt):
    """This Function is cheking count of 'from' and 'to'. They must be equal:"""

    counter = 0
    ind = 0
    while ind != len(txt):
        if "for" in txt[ind]:
            splitted_row = list_of_text[ind].split()
            for line in splitted_row:
                if "from" in line:
                    counter += 1
                elif "to" in line:
                    counter -= 1
        ind += 1

    if counter != 0:
        raise SyntaxError("Number of 'from' and 'to' must be equal:")


def creating_variable_for(arg):
    """This function assign value in variable."""

    for i in range(3, len(arg)):
        if arg[i] in variable_dict:
            arg[i] = str(variable_dict[arg[i]])
    variable_dict[arg[1]] = eval(" ".join(arg[3]))


def variable_after_declaring_for(idx):
    """A function that performs the following assignment operations for 'for' loop"""

    arg = list_of_text[idx].split()
    if arg[0] in variable_dict and arg[1] == "from":
        for i in range(2, len(arg)):
            if arg[i] in variable_dict:
                arg[i] = str(variable_dict[arg[i]])
        variable_dict[arg[0]] = eval(" ".join(arg[2:]))


def is_declared_for(idx):
    """This function ceking Is the variable declared? for 'for' loop"""

    row = list_of_text[idx].split()
    for i in range(5):
        if row[0] in variable_dict or ["for", "!"][i] in row[0]:
            return True

    raise NameError(f"Name ({str(row[0])})' is unrecognizable.")


def after_for(idx):
    """This function is checking, or does FOR ends with '!'"""

    if "!" not in list_of_text[idx:]:
        raise SyntaxError("After FOR you mast end with !")


def already_declared_for(idx):
    """ This function is cheking, that declared variables were been declared. """

    row = list_of_text[idx].split()
    if row[1] in variable_dict:
        variable_dict[row[1]] = variable_dict[row[1]] + 1


def for_in_dict():
    """This function do file line by line when reach a line that starts 'for'
    and will do untill will reach line that ends with '!' and adds the variable 
    declared in that line to our total dict'"""

    ind = 0
    while ind != len(list_of_text):
        if "for" in list_of_text[ind]:
            splitted_row = list_of_text[ind].split()
            splitted_row_1 = splitted_row[1:]

            if "var" in splitted_row_1:
                creating_variable_for(splitted_row_1)
                variable_name(splitted_row_1)
                variable_after_declaring_for(ind)
                already_declared_for(ind)
                after_for(ind)

        ind += 1


def have_for():
    """This function do file line by line when reach a line that starts 'for'
    and will do untill will reach line that ends with '!''"""

    ind = 0

    while ind != len(list_of_text):
        if "for" in list_of_text[ind]:
            splitted_row = list_of_text[ind].split()
            key = splitted_row[2]
            while int(splitted_row[-3]) < int(splitted_row[-1]):
                for_in_dict()
                variable_dict[key] = int(splitted_row[-3])
                splitted_row[-3] = str(int(splitted_row[-3]) + 1)

                print(variable_dict[key])

                after_for(ind)
                variable_value(splitted_row)
                while list_of_text[ind] != "!":
                    ind += 1

                if ind != len(list_of_text):
                    untill_if_while_for(ind)

                else:
                    while "!" not in list_of_text[ind]:
                        ind += 1
                    untill_if_while_for(ind)

        ind += 1


is_syntax_right(list_of_text)
is_syntax_right_from_to(list_of_text)
untill_if_while_for()
have_if()
do_while()
have_for()
print(variable_dict)