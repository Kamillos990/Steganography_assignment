import random


class Substitution:

    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def makeKey(alphabet : str) -> str:
        """generates key to encrypt message
        Args:
            alphabet[str]: string containing all letters in alphabetical order
        Returns:
            key[str]: string with shuffled elements of alphabet
        """
        alphabet = list(alphabet)
        random.shuffle(alphabet)
        key = ''.join(alphabet)
        return key

    def encrypt(message: str, key:str, alphabet:str) ->str:
        """encrypts message using substitution algorithm
        Args:
            message[str]: message to encrypt
            key[str]: string with shuffled elements of alphabet
            alphabet[str]: string containing all letters in alphabetical order
        Returns:
            encrypted message all in lowercase [str]
        """

        keyMap = dict(zip(alphabet, key))
        return ''.join(keyMap.get(c.lower(), c) for c in message)

    def decrypt(cipher: str, key:str, alphabet:str) -> str:
        """decrypts message encrypted using substitution algorithm
        Args:
            cipher[str]: encrypted message
            key[str]: key used to encrypt message
            alphabet[str]: string containing all letters in alphabetical order
        Returns:
            decrypted message all in lowercase [str]
        """
        keyMap = dict(zip(key, alphabet))
        return ''.join(keyMap.get(c.lower(), c) for c in cipher)
