from hashlib import sha256
from math import ceil
import secrets
from typing import List, Tuple

DEFAULT_BIT_LENGTH = 2048


def hash_number(n: int) -> int:
    pass


class PSIAgent:
    def __init__(
        self, initial_set: List[int], p: int, bit_length: int = DEFAULT_BIT_LENGTH
    ) -> None:
        pass

    def prepare_intermediate_keys(self) -> List[int]:
        pass


class PSIServer(PSIAgent):
    def handle_request(
        self, client_intermediate_keys: List[int]
    ) -> Tuple[List[int], List[int]]:
        pass


class PSIClient(PSIAgent):
    def handle_response(
        self, client_keys: List[int], server_intermediate_keys: List[int]
    ) -> List[int]:
        pass
