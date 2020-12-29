from typing import Any, Optional


class Encoder:
    """
    Encode data to bencoding format
    Info about format: https://en.wikipedia.org/wiki/Bencode
    Allowed types are:
        - int
        - str
        - list
        - dict
        - bytes

    Other types will be ignored.
    """

    def __init__(self, data: Any) -> None:
        super().__init__()
        self.data = data

    @staticmethod
    def _encode_int(n: int) -> bytes:
        return f"i{n}e".encode()

    @staticmethod
    def _encode_str(s: str) -> bytes:
        return f"{len(s)}:{s}".encode()

    @staticmethod
    def _encode_bytes(b: bytes) -> bytes:
        result = bytearray()
        result += str.encode(str(len(b)))
        result += b":"
        result += b
        return result

    def _encode_list(self, lst: list) -> bytes:
        res = b"".join(
            [self._encode_next(element) for element in lst if element is not None]  # type: ignore
        )
        res = b"l" + res + b"e"
        return res

    def _encode_dict(self, d: dict) -> bytes:
        res = b""
        for key, value in d.items():
            k = self._encode_next(key)
            v = self._encode_next(value)
            if k and v:
                res = res + k + v
        res = b"d" + res + b"e"
        return res

    def _encode_next(self, data: Any) -> Optional[bytes]:
        if type(data) == int:
            return self._encode_int(data)
        elif type(data) == str:
            return self._encode_str(data)
        elif type(data) == list:
            return self._encode_list(data)
        elif type(data) == dict:
            return self._encode_dict(data)
        elif type(data) == bytes:
            return self._encode_bytes(data)
        else:
            return None

    def encode(self) -> Optional[bytes]:
        return self._encode_next(self.data)


class Decoder:
    def __init__(self, raw: bytes) -> None:
        super().__init__()
        self.raw = raw
        self._index = 0

    def _read_until(self, symbol: bytes) -> bytes:
        start_index = self._index
        self._index = self.raw.index(symbol, self._index) + 1
        return self.raw[start_index : self._index - 1]

    def _read_next(self, n: int, move_index: bool = True) -> bytes:
        start_position = self._index
        if move_index:
            self._index += n
        return self.raw[start_position : start_position + n]

    def _decode_int(self) -> int:
        return int(self._read_until(b"e"))

    def _decode_str(self) -> str:
        length = int(self._read_until(b":"))
        return self._read_next(length).decode()

    def _decode_list(self) -> list:
        res = []
        while self.raw[self._index : self._index + 1] != b"e":
            res.append(self.decode())
        return res

    def _decode_dict(self) -> dict:
        res = {}
        while self.raw[self._index : self._index + 1] != b"e":
            key = self.decode()
            res[key] = self.decode()
        return res

    def decode(self) -> Any:
        """
        Decode bencoded data to python object
        """

        current = self._read_next(1, False)

        print(f"Current: {str(current)}")
        if current == b"i":
            self._read_next(1)
            return self._decode_int()
        elif current in b"1234567890":
            return self._decode_str()
        elif current == b"l":
            self._read_next(1)
            return self._decode_list()
        elif current == b"d":
            self._read_next(1)
            return self._decode_dict()
        else:
            return None
