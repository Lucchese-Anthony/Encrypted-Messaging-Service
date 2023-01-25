# Encrypted Messaging Service

# Overview 

This program is a python-based socket connection messaging service utilizing RSA encryption for end-to-end encryption of messages between a server and a client

To run the program, you need to create 5 text files:
- ip.txt
- pCLient.txt
- qClient.txt
- pServer.txt
- qServer.txt

the `ip.txt` file holds the ip or url of the host to bind to for the server

the other files hold a prime self that will be used to encrypt the messages

## Documentation for Sympy totient
```python
class totient(Function):
    @classmethod
    def eval(cls, n):
        if n.is_Integer:
            if n < 1:
                raise ValueError("n must be a positive integer")
            factors = factorint(n)
            return cls._from_factors(factors)
        elif not isinstance(n, Expr) or (n.is_integer is False) or (n.is_positive is False):
            raise ValueError("n must be a positive integer")

    def _eval_is_integer(self):
        return fuzzy_and([self.args[0].is_integer, self.args[0].is_positive])

    @classmethod
    def _from_distinct_primes(self, *args):
        """Subroutine to compute totient from the list of assumed
        distinct primes
        Examples
        ========
        >>> from sympy.ntheory.factor_ import totient
        >>> totient._from_distinct_primes(5, 7)
        24
        """
        return reduce(lambda i, j: i * (j-1), args, 1)

    @classmethod
    def _from_factors(self, factors):
        """Subroutine to compute totient from already-computed factors
        Examples
        ========
        >>> from sympy.ntheory.factor_ import totient
        >>> totient._from_factors({5: 2})
        20
        """
        t = 1
        for p, k in factors.items():
            t *= (p - 1) * p**(k - 1)
        return t
    ```

