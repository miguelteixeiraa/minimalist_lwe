from random import randint
from collections.abc import Iterable
from typing import List, Tuple, Any
from math import floor


class MinimalistLWE:
    def __init__(self, q: int, n: int):
        # stuff to generate public key
        self._prime_q = q
        self._integer_n = n

        # keys
        self._privateKey: int = self.gen_privateKey()
        self._publicKey: Tuple[List[int], List[int]] = self.gen_publicKey()

    #

    def gen_privateKey(self) -> int:
        return randint(1, 99999)

    #

    def gen_publicKey(self) -> Tuple[List[int], List[int]]:
        A: List[int] = []
        E: List[int] = []
        B: List[int] = []

        # defining A
        for n in range(0, self._integer_n):
            A.append(randint(1, self._prime_q))
        #

        # definig errors
        for n in range(0, self._integer_n):
            E.append(randint(1, 4))
        #

        # and then, defining B
        for n in range(0, self._integer_n):
            B.append((A[n] * self._privateKey + E[n]) % self._prime_q)
        #

        return (A, B)

    #

    def _perform_u_v(self, bit: int):
        u: int = 0
        v: int = 0

        sumASamples: int = 0
        sumBSamples: int = 0

        number_of_samples = randint(2, self._integer_n)

        prev_index = 0
        for selectedSample in range(0, number_of_samples):
            index = randint(0, self._integer_n - 1)
            while prev_index == index:
                index = randint(0, self._integer_n - 1)
            #
            sumASamples += self._publicKey[0][index]
            sumBSamples += self._publicKey[1][index]
            prev_index = index
        #

        u = sumASamples % self._prime_q
        v = sumBSamples - (self._prime_q / 2) * bit
        v = v % self._prime_q

        return (u, v)

    #

    def min_encrypt(self, message: Any):
        encrypted_message: List[Tuple[int]] = []
        message_encoding: List[str] = []
        identified_type: str = ""
        if isinstance(message, Iterable):
            if type(message) == str:
                for char in message:
                    message_encoding.append(ord(char))
                    identified_type = "text"
                #
            elif isinstance(message, List):
                for element in message:
                    if isinstance(element, int) or isinstance(element, float):
                        message_encoding.append("{0:b}".format(element))
                        identified_type = "number list"
                    #
                #
            #
        elif isinstance(message, int) or isinstance(message, float):
            message_encoding.append("{0:b}".format(message))
            identified_type = "single number"
        #

        if identified_type == "":
            return "it's unable to identify what you are trying to evaluate"
        #

        elif identified_type == "single number":
            for number in message_encoding:
                for bit in number:
                    # encrypt each bit
                    encrypted_message.append(self._perform_u_v(int(bit)))
                #
        #

        return encrypted_message

    #

    def min_decrypt(self, cyphertext: List[Tuple[int]], sk: int) -> Any:
        decrypted_message = ""
        for element in cyphertext:
            tmp_dec = (element[1] - sk * element[0]) % self._prime_q
            if tmp_dec < self._prime_q / 2:
                decrypted_message += "0"
            else:
                decrypted_message += "1"
            #
        #
        return int(decrypted_message, 2)

    #

    def get_privateKey(self):
        return self._privateKey

    #


#

if __name__ == "__main__":
    minimalistLWE = MinimalistLWE(97, 100)
    minimalistLWE.gen_publicKey()

    sk = minimalistLWE.get_privateKey()

    encrypted_message = minimalistLWE.min_encrypt(90)

    print(f"cyphertext: {encrypted_message}")

    decrypted_message = minimalistLWE.min_decrypt(encrypted_message, sk)

    print(f"plaintext again: {decrypted_message}")
