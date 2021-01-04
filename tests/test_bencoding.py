from bencoding import Encoder


def test_encode_int() -> None:
    assert Encoder(123).encode() == b"i123e"


def test_encode_negative() -> None:
    assert Encoder(-1).encode() == b"i-1e"


def test_encode_zero() -> None:
    assert Encoder(0).encode() == b"i0e"


def test_encode_str() -> None:
    encode_text = "Some random string"
    assert Encoder(encode_text).encode() == f"{len(encode_text)}:{encode_text}".encode()


def test_encode_list() -> None:
    encode_list = [1, 2, "ste"]
    assert Encoder(encode_list).encode() == f"li1ei2e3:stee".encode()


def test_encode_dict() -> None:
    encode_dict = {"str": "ste", 1: 1, 2: ["one", "two"]}

    assert (
        Encoder(encode_dict).encode() == f"d3:str3:stei1ei1ei2el3:one3:twoee".encode()
    )
