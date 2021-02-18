from hashlib import sha256
from math import ceil
import secrets
from typing import List, Tuple

DEFAULT_BIT_LENGTH = 2048  # For the secret exponents


def hash_number(n: int) -> int:
    n_bytes = n.to_bytes(ceil(n.bit_length() / 8), byteorder="big", signed=False)
    hashed_bytes = sha256(n_bytes).digest()
    return int.from_bytes(hashed_bytes, byteorder="big", signed=False)


class PSIAgent:
    def __init__(
        self, initial_set: List[int], p: int, bit_length: int = DEFAULT_BIT_LENGTH
    ) -> None:
        self.set = initial_set
        self.p = p
        key_space = 2 ** bit_length
        self.secret = secrets.randbelow(key_space)

    def is_generator(self, g: int) -> bool:
        p = self.p
        l = len(set([pow(g, i, p) for i in range(1, p)]))
        return l == p - 1

    def exponentiate(self, g: int) -> int:
        return pow(g, self.secret, self.p)

    def prepare_intermediate_key(self, n: int) -> int:
        hashed_n = hash_number(n)
        return (
            self.exponentiate(hashed_n)
            if self.is_generator(hashed_n)
            else self.prepare_intermediate_key(hashed_n)
        )

    def prepare_intermediate_keys(self) -> List[int]:
        return [self.prepare_intermediate_key(n) for n in self.set]


class PSIServer(PSIAgent):
    def handle_request(
        self, client_intermediate_keys: List[int]
    ) -> Tuple[List[int], List[int]]:  # (client_keys, server_intermediate_keys)
        client_keys = [self.exponentiate(n) for n in client_intermediate_keys]
        server_intermediate_keys = self.prepare_intermediate_keys()
        return client_keys, server_intermediate_keys


class PSIClient(PSIAgent):
    def handle_response(
        self, client_keys: List[int], server_intermediate_keys: List[int]
    ) -> List[int]:
        server_keys = [self.exponentiate(n) for n in server_intermediate_keys]
        return [n for key, n in zip(client_keys, self.set) if key in server_keys]
