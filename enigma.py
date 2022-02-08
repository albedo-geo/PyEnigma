import random


class Plugboard:
    def __init__(self, seed: int, num_pairs: int) -> None:
        nums = list(range(26))  # [1,2,3,...,24,25]
        random.seed(seed)
        random.shuffle(nums)  # [3,7,5,...,1,16]
        self.code = {}
        for i in range(0, num_pairs * 2, 2):
            a, b = nums[i : i + 2]
            self.code[a] = b
            self.code[b] = a

    def reflect(self, letter: str) -> str:
        assert len(letter) == 1
        idx = ord(letter) - 65  # ASCII
        if idx in self.code:
            return chr(self.code[idx] + 65)
        return letter


class Reflector(Plugboard):
    def __init__(self, seed: int) -> None:
        super().__init__(seed, 13)


class Rotor:
    def __init__(self, seed: int, shift: int = 0) -> None:
        self.code = list(range(26))  # [1,2,3,...,24,25]
        self.shift = shift
        random.seed(seed)
        random.shuffle(self.code)  # [3,7,5,...,1,16]

    def forward(self, letter: str) -> str:
        assert len(letter) == 1
        idx = ord(letter) - 65  # ASCII
        idx = (idx + self.shift) % 26
        return chr(self.code[idx] + 65)

    def backward(self, letter: str) -> str:
        assert len(letter) == 1
        idx = ord(letter) - 65  # ASCII
        idx = (self.code.index(idx) - self.shift) % 26
        return chr(idx + 65)

    def step(self) -> bool:
        self.shift += 1
        if self.shift == 26:
            self.shift = 0
            return True
        return False


class Enigma:
    def __init__(self, rotors, reflector, plugboard) -> None:
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard

    def process(self, letter: str) -> str:
        assert len(letter) == 1
        letter = self.plugboard.reflect(letter)
        for rotor in self.rotors:
            letter = rotor.forward(letter)
        letter = self.reflector.reflect(letter)
        for rotor in reversed(self.rotors):
            letter = rotor.backward(letter)
        letter = self.plugboard.reflect(letter)
        self.step()
        return letter

    def process_many(self, sentence: str) -> str:
        return "".join([self.process(letter) for letter in sentence])

    def step(self) -> None:
        for rotor in self.rotors:
            carry = rotor.step()
            if not carry:
                break
        # print([rotor.shift for rotor in self.rotors])


message = 'HELLOWORLD'


def get_enigma():
    rotor1 = Rotor(1334, 20)
    rotor2 = Rotor(1335, 3)
    rotor3 = Rotor(1336, 1)
    reflector = Reflector(1337)
    plugboard = Plugboard(1338, 6)
    enigma = Enigma([rotor1, rotor2, rotor3], reflector, plugboard)
    return enigma


enigma1 = get_enigma()
enigma2 = get_enigma()

encrpyted = enigma1.process_many(message)
decrpyted = enigma2.process_many(encrpyted)

print(encrpyted)
print(decrpyted)
