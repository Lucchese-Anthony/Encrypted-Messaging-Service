import unittest
from equations import *
import string
import random

#python3 -m unittest -v test.Testing


p = 953
q = 359
n = 342127
phi_of_n = 340816
e = 49213
d = 2133


class Testing(unittest.TestCase):

    def test_combine_numbers_into_one_number(self) -> None:
        return

    def test_get_phi_of_n(self):
        test = get_phi_of_a_prime(p, q)
        self.assertEqual(test, phi_of_n)

    def test_phi(self):
        test = phi(n)
        self.assertEqual(get_phi_of_a_prime(p, q), test)


    def test_euclidean_algorithm(self):
        test = euclidean_algorithm(p, q)
        self.assertEqual(1, test)

    def test_find_exponent_modulo_n(self):
        test = find_exponent_modulo_n(p, q, n)
        self.assertEqual(953, test)

    def test_find_d(self):
        test = find_d(49213, phi_of_n, n)
        self.assertEqual(d, test)

    def test_if_string_conversion_works(self):
        rand: int = random.randint(10, 20)
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=rand))
        self.assertEqual(res, convertNumberToString(convertStringToNumber(res)))

    def test_decrypt_message(self):
        test = decrypt_message((convertStringToNumber('HELLO') ** 7 % 323), 247, 323)
        self.assertEqual('HELLO', test)

    def test_encrypt_message(self):
        test = encrypt_message("J", 7, 323)
        self.assertEqual(10**7 % 323, test)

    def test_message_encrypt_decrypt(self):
        encrypted_message = encrypt_message("HELLO", e, n)
        print(encrypted_message)
        test = decrypt_message(encrypted_message, d, n)
        print(test)
        self.assertEqual("HELLO", test)


if __name__ == '__main__':
    unittest.main()
