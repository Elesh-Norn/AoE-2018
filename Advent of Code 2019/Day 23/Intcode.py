from collections import deque
class Outcode:

    __slots__ = ["opcode", "mode1", "mode2", "mode3", "input_1", "input_2", "output"]

    def __init__(self, intcodes, pointer, base):
        outcode = str(intcodes[pointer])
        self.opcode = int(outcode[-2:])
        self.mode1 = int(outcode[-3]) if len(outcode) > 2 else 0
        self.mode2 = int(outcode[-4]) if len(outcode) > 3 else 0
        self.mode3 = int(outcode[-5]) if len(outcode) > 4 else 0
        if self.opcode < 3 or 99 > self.opcode > 4:

            if self.mode1 == 0:
                adress = intcodes[pointer + 1]
            elif self.mode1 == 1:
                adress = pointer + 1
            elif self.mode1 == 2:
                adress = intcodes[pointer + 1] + base

            intcodes = self.memory_check(adress, intcodes)
            self.input_1 = intcodes[adress]

            if self.opcode != 9:
                if self.mode2 == 0:
                    adress = intcodes[pointer + 2]
                elif self.mode2 == 1:
                    adress = pointer + 2
                elif self.mode2 == 2:
                    adress = intcodes[pointer + 2] + base

                intcodes = self.memory_check(adress, intcodes)
                self.input_2 = intcodes[adress]

    def add(self, intcodes: list, pointer: int, base: int)->int:
        adress = intcodes[pointer + 3] + base if self.mode3 == 2 else intcodes[pointer + 3]
        intcodes = self.memory_check(adress, intcodes)
        intcodes[adress] = self.input_1 + self.input_2

        return pointer + 4

    def mul(self, intcodes: list, pointer: int, base: int)->int:
        adress = intcodes[pointer + 3] + base if self.mode3 == 2 else intcodes[pointer + 3]
        intcodes = self.memory_check(adress, intcodes)
        intcodes[adress] = self.input_1 * self.input_2

        return pointer + 4

    def read_input(self, intcodes: list, pointer: int, base: int, robocode:int)->int:
        adress = intcodes[pointer + 1] + base if self.mode1 == 2 else intcodes[pointer + 1]

        intcodes = self.memory_check(adress, intcodes)
        intcodes.append(0)
        intcodes[adress] = robocode
        return pointer + 2

    def print_output(self, intcodes: list, pointer: int, base: int)->int:
        if self.mode1 == 0:
            adress = intcodes[pointer + 1]
        elif self.mode1 == 1:
            adress = pointer + 1
        else:
            adress = intcodes[pointer + 1] + base

        intcodes = self.memory_check(adress, intcodes)
        self.output = intcodes[adress]
        return pointer + 2

    def is_less_than(self, intcodes: list, pointer: int, base: int)->int:
        if self.mode3 == 0:
            adress = intcodes[pointer + 3]
        else:
            adress = intcodes[pointer + 3] + base

        intcodes = self.memory_check(adress, intcodes)
        intcodes[adress] = 1 if self.input_1 < self.input_2 else 0
        return pointer + 4

    def is_equal_to(self, intcodes: list, pointer: int, base: int)->int:
        if self.mode3 == 0:
            adress = intcodes[pointer + 3]
        else:
            adress = intcodes[pointer + 3] + base

        intcodes = self.memory_check(adress, intcodes)
        intcodes[adress] = 1 if self.input_1 == self.input_2 else 0
        return pointer + 4


    def jump_if_false(self, intcodes, pointer: int, base: int)->int:

        if self.input_1 != 0:
            return self.input_2
        else:
            return pointer + 3

    def jump_if_true(self, intcodes, pointer: int, base: int)->int:
        if self.input_1 == 0:
            return self.input_2
        else:
            return pointer + 3

    def ofset_base(self, intcodes, pointer: int, base: int)->(int, int):
        base += self.input_1
        return pointer + 2, base

    def memory_check(self, adress, intcodes):
        if adress >= len(intcodes):
            for x in range(adress - len(intcodes)):
                intcodes.append(0)
            intcodes.append(0)
            return intcodes
        return intcodes

class Computer:

    __slots__ = ["intcodes", "pointer", "output", "phase", "base", "input_queue", "function_dico", "idle"]

    def __init__(self, intcode:list):

        self.intcodes = intcode
        self.pointer = 0
        self.input_queue = deque()
        self.idle = False
        self.output = []
        self.phase = False
        self.base = 0
        self.function_dico = {
            1: Outcode.add,
            2: Outcode.mul,
            3: Outcode.read_input,
            4: Outcode.print_output,
            5: Outcode.jump_if_false,
            6: Outcode.jump_if_true,
            7: Outcode.is_less_than,
            8: Outcode.is_equal_to,
            9: Outcode.ofset_base
        }

    def run(self, robotcode=None)->(int, bool):
        if robotcode is not None:
            self.idle = False
            for element in robotcode:
                self.input_queue.append(element)


        outcode = Outcode(self.intcodes, self.pointer, self.base)
        if outcode.opcode == 99:
            return 99

        elif 0 < outcode.opcode < 10:
            if outcode.opcode == 3:
                if len(self.input_queue) > 0:
                    self.idle = False
                else:
                    self.idle = True
                self.pointer = self.function_dico[outcode.opcode](outcode,
                                                                  self.intcodes,
                                                                  self.pointer,
                                                                  self.base,
                                                                  self.input_queue.popleft()
                                                                  if len(self.input_queue) > 0 else -1)

            elif outcode.opcode == 4:
                self.pointer = self.function_dico[outcode.opcode](outcode,
                                                                  self.intcodes,
                                                                  self.pointer,
                                                                  self.base)
                self.output.append(outcode.output)
                if len(self.output) > 2:
                    send = self.output
                    self.output = deque()
                    return send

            elif outcode.opcode == 9:
                self.pointer, self.base = self.function_dico[outcode.opcode](outcode,
                                                              self.intcodes,
                                                              self.pointer,
                                                              self.base)
            else:
                self.pointer = self.function_dico[outcode.opcode](outcode,
                                                                  self.intcodes,
                                                                  self.pointer,
                                                                  self.base)

        else:
            print("Something went wrong!")
            return 99

        return self.idle