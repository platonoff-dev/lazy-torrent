from meta_file.bencoding import Decoder, Encoder


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
    assert Encoder(encode_list).encode() == "li1ei2e3:stee".encode()


def test_encode_dict() -> None:
    encode_dict = {"str": "ste", 1: 1, 2: ["one", "two"]}

    assert Encoder(encode_dict).encode() == "d3:str3:stei1ei1ei2el3:one3:twoee".encode()


def test_encode_bytes() -> None:
    encode_bytes = b"123456"
    assert Encoder(encode_bytes).encode() == bytearray(
        f"{len(encode_bytes)}:{encode_bytes.decode()}".encode()
    )


def test_decode_int() -> None:
    assert Decoder(b"i123e").decode() == 123


def test_decode_str() -> None:
    decode_bytes = b"5:qwert"
    assert Decoder(decode_bytes).decode() == "qwert"


def test_decode_list() -> None:
    decode_bytes = b"li1ei2e3:stee"
    assert Decoder(decode_bytes).decode() == [1, 2, "ste"]


def test_decode_dict() -> None:
    decode_bytes = b"d3:str3:stei1ei1ei2el3:one3:twoee"
    assert Decoder(decode_bytes).decode() == {"str": "ste", 1: 1, 2: ["one", "two"]}


def test_encode_none() -> None:
    assert Encoder(None).encode() is None


def test_decode_none() -> None:
    assert Decoder(b"fghfgh").decode() is None
