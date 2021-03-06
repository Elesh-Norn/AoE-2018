def read_input():
    intcodes = []
    with open('Day_5_input.txt', "r") as file:
        for x in file:
            s = x.split(",")
            for ints in s:
                intcodes.append(int(ints))
    return intcodes


class Outcode:

    def __init__(self, intcodes, pointer):
        outcode = str(intcodes[pointer])
        self.opcode = int(outcode[-2:])
        self.mode1 = int(outcode[-3]) if len(outcode) > 2 else 0
        self.mode2 = int(outcode[-4]) if len(outcode) > 3 else 0
        self.mode3 = int(outcode[-5]) if len(outcode) > 4 else 0
        if self.opcode < 3 or 99 > self.opcode > 4:
            self.input_1 = intcodes[intcodes[pointer + 1]] if self.mode1 == 0 else intcodes[pointer + 1]
            self.input_2 = intcodes[intcodes[pointer + 2]] if self.mode2 == 0 else intcodes[pointer + 2]

    def add(self, intcodes, pointer):
        intcodes[intcodes[pointer + 3]] = self.input_1 + self.input_2
        return pointer + 4

    def mul(self, intcodes, pointer):
        intcodes[intcodes[pointer + 3]] = self.input_1 * self.input_2
        return pointer + 4

    def read_input(self, intcodes, pointer):
        if self.mode1 == 0:
            intcodes[intcodes[pointer + 1]] = int(input("Please input a digit"))
        else:
            intcodes[pointer + 1] = int(input("Please input a digit"))
        return pointer + 2

    def print_output(self, intcodes, pointer):
        output = intcodes[intcodes[pointer + 1]] if self.mode1 == 0 else intcodes[pointer + 1]
        print(output)
        return pointer + 2

    def is_less_than(self, intcodes, pointer):
        intcodes[intcodes[pointer + 3]] = 1 if self.input_1 < self.input_2 else 0
        return pointer + 4

    def is_equal_to(self, intcodes, pointer):
        intcodes[intcodes[pointer + 3]] = 1 if self.input_1 == self.input_2 else 0
        return pointer + 4

    def jump_if_false(self, intcodes, pointer):
        if self.input_1 != 0:
            return self.input_2
        else:
            return pointer + 3

    def jump_if_true(self, intcodes, pointer):
        if self.input_1 == 0:
            return self.input_2
        else:
            return pointer + 3

def read_intcodes(intcodes):
    pointer = 0
    function_dico = {
        1: Outcode.add,
        2: Outcode.mul,
        3: Outcode.read_input,
        4: Outcode.print_output,
        5: Outcode.jump_if_false,
        6: Outcode.jump_if_true,
        7: Outcode.is_less_than,
        8: Outcode.is_equal_to,
    }

    while True:
        outcode = Outcode(intcodes, pointer)
        if outcode.opcode == 99:
            return intcodes

        elif 0 < outcode.opcode < 9:
            pointer = function_dico[outcode.opcode](outcode, intcodes, pointer)

        else:
            print("Something went wrong!")
            return None


test1 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
read_intcodes(test1)
