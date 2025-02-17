"""
This module define a transaction class. A transaction is a message signed by a private key.
The signature can be verified with the public key.

A transaction is a dictionary with the following keys:
    - message: the message to sign
    - date: the date of the transaction
    - author: the hash of the public key
    - vk: the public key
    - signature: the signature of the message

The signature and the public key are binary strings. Both are converted to hexadecimal (base64) string to be
stored in the transaction.

The hash of the transaction is the hash of the dictionary (keys are sorted).
"""

import proj_utils
import json
import hashlib
from ecdsa import VerifyingKey, BadSignatureError
from rich.console import Console
from rich.table import Table


class IncompleteTransaction(Exception):
    pass


class Transaction(object):
    def __init__(self, container_id, event, info, harbor=None, ship=None, date=None):
        """
        Initialize a transaction. If date is None, the current time is used.
        Signature and verifying key may be None.

        Author is the hash of the verifying key (or None if vk is not specified).

        :param message: str
        :param date: str in format "%Y-%m-%d %H:%M:%S.%f" see (module "utils")
        :param signature: str
        :param vk: str
        """
        
        self.container_id = container_id  # Identifiant unique du conteneur
        self.event = event  # Description de l'événement (par exemple, "Chargement", "Arrivée")
        self.timestamp = date or proj_utils.get_time() # Date et heure de l'événement
        self.ship = ship #Navire où se situe le conteneur
        self.harbor = harbor #Port où se situe le conteneur
        self.info = info #Dictionnaire de caractéristique du conteneur : taille, propriétaire, 
    

    def json_dumps(self):
        """
        Return a json representation of the transaction. The keys are sorted.
        :return:
        """
        return json.dumps(self.data, sort_keys=True)

    @property
    def data(self):
        d = {
            "container_id": self.container_id,
            "event": self.event,
            "author": self.author,
            "vk": self.vk
        }
        return d

    def sign(self, sk):
        """
        Sign a transaction with a signing key. Set both attributes "signature" and "vk"
        :param sk: A signing key (private)
        """
        json_data = self.json_dumps()
        signature = sk.sign(json_data.encode()).hex()
        self.signature = signature
        self.vk = sk.verifying_key.to_pem().hex()
        self.author = hashlib.sha256(self.vk.encode()).hexdigest()

    def verify(self):
        """
        Verify the signature of the transaction and the author.
        :return: True or False
        """
        try:
            vk = VerifyingKey.from_pem(bytes.fromhex(self.vk))
            binary_signature = bytes.fromhex(self.signature)
            data = self.json_dumps().encode()

            # Si la vérification réussit, renvoyer True
            return vk.verify(binary_signature, data)

        except Exception as e:
            # En cas d'erreur, renvoyer False au lieu de lever une exception
            print(f"Échec de la vérification: {e}")
            return False

    def __str__(self):
        """
        :return: A string representation of the transaction
        """
        return f"Transaction(message={self.message}, date={self.date}, author={self.author}, vk={self.vk}, signature={self.signature})"

    def __lt__(self, other):
        """
        Compare two transactions. The comparison is based on the hash of the transaction if it is defined else, the date.
        :param other: a transaction
        :return: True or False
        """
        
        self_hash = hashlib.sha256(self.json_dumps().encode()).hexdigest()
        other_hash = hashlib.sha256(other.json_dumps().encode()).hexdigest()

        if self_hash and other_hash:
            return self_hash < other_hash
        else:
            return self.date < other.date


    def hash(self):
        """
        Compute the hash of the transaction.

        :raise IncompleteTransaction: if the transaction is not complete (signature or vk is None)
        :return:
        """
        
        if self.signature is None or self.vk is None:
            raise IncompleteTransaction("La transaction est incomplète : la signature ou la clef de vérification est manquante.")

        data_to_hash = self.json_dumps() + str(self.signature) + str(self.vk) + str(self.message) + str(self.date) +  str(self.author)

        return hashlib.sha256(data_to_hash.encode()).hexdigest()

    @staticmethod
    def log(transactions):
        """
        Print a nice log of set of the transactions
        :param transactions:
        :return:
        """
        table = Table(title=f"List of transactions")
        table.add_column("Hash", justify="left", style="cyan")
        table.add_column("Message", justify="left", style="cyan")
        table.add_column("Date", justify="left", style="cyan")
        table.add_column("Signature", justify="left", style="cyan")
        table.add_column("Author", justify="left", style="cyan")

        for t in sorted(transactions):
            table.add_row(
                None if t.vk is None else t.hash()[:14] + "...",
                t.message,
                t.date[:-7],
                None if t.signature is None else t.signature[:7] + "...",
                None if t.author is None else t.author[:7] + "..."
            )

        console = Console()
        console.print(table)


def test0():
    from ecdsa import SigningKey, NIST384p
    sk = SigningKey.generate(curve=NIST384p)
    t1 = Transaction("One")
    t2 = Transaction("Two")
    t3 = Transaction("Three")
    t4 = Transaction("Four")
    t3.sign(sk)
    t4.sign(sk)
    Transaction.log([t1, t2, t3, t4])


def test1():
    from ecdsa import SigningKey, NIST384p
    sk = SigningKey.generate(curve=NIST384p)
    t = Transaction("Message de test")
    print(t)
    t.sign(sk)
    print(t)
    print(t.hash())
    print(t.vk)
    print(t.verify())
    t.message += "2"
    print(t.verify())


def test2():
    """
    Warning: sk.verifying_key.to_pem().hex() produce a long string starting and ending with common information.
    It is easy to manually check that the two strings are different, but it is not easy to see the difference.
    This is the reason why the hash of the public key is used for author instead of the public key itself.
    """
    from ecdsa import SigningKey
    sk = SigningKey.generate()
    sk2 = SigningKey.generate()
    print(sk.verifying_key.to_pem().hex())
    print(sk2.verifying_key.to_pem().hex())
    print(sk.verifying_key.to_pem().hex() == sk2.verifying_key.to_pem().hex())


if __name__ == "__main__":
    print("Test Transaction")
    test0()
    #test1()
    #test2()

