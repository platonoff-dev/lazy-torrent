from typing import Any, Optional, Union


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

    def _read_until_element(self, element: bytes) -> bytes:
        start_index = self._index
        self._index = self.raw.index(element, self._index) + 1
        return self.raw[start_index : self._index - 1]

    def _read(self, n: int) -> bytes:
        return self.raw[self._index : self._index + n]

    def _consume(self, n: int) -> bytes:
        start_position = self._index
        self._index = self._index + n
        return self.raw[start_position : self._index]

    def _decode_int(self) -> int:
        return int(self._read_until_element(b"e"))

    def _decode_str(self) -> Union[str, bytes]:
        length = int(self._read_until_element(b":"))
        str_data: Union[bytes, str]
        try:
            str_data = self._read(length).decode()
        except UnicodeDecodeError:
            str_data = self._read(length)
        self._consume(length)
        return str_data

    def _decode_list(self) -> list:
        res = []
        while self.raw[self._index : self._index + 1] != b"e":
            res.append(self.decode())
        self._consume(1)
        return res

    def _decode_dict(self) -> dict:
        res = {}
        while self.raw[self._index : self._index + 1] != b"e":
            key = self.decode()
            res[key] = self.decode()
        self._consume(1)
        return res

    def decode(self) -> Any:
        current = self._read(1)
        if current == b"i":
            self._consume(1)
            return self._decode_int()
        elif current in b"1234567890":
            return self._decode_str()
        elif current == b"l":
            self._consume(1)
            return self._decode_list()
        elif current == b"d":
            self._consume(1)
            return self._decode_dict()
        else:
            return None
