from rake.core.dbhelper import Doc


def serialize_integer(val: int):
    """
    Format: integer -> byte array'size|bytes_in_memory'

    :param val: Integer val to be serialized
    :return: bytes_of_val: The serialized bytes
    """

    bytes_of_val = bytearray()
    size_of_val = 0
    tmp = val if val > 0 else -val

    # append one byte to seize a seat for num of bytes in val
    bytes_of_val.append(0)
    # copy bytes in the memory of val
    while tmp != 0:
        bytes_of_val.append(tmp & 0xFF)
        size_of_val += 1
        tmp >>= 8
    # update the size and the first bit in size represents sign: 0 for +
    bytes_of_val[0] = size_of_val if val > 0 else (size_of_val | 0x80)

    return bytes_of_val


def deserialize_integer(byte_stream: bytearray, offset=0):
    """
    Deserialize from serialized integer

    :param byte_stream: Bytes where the serialized integer stored
    :param offset: Offset of the serialized integer in %byte_stream
    :returns: Offset and target val
    """

    val = 0

    # size of bytes which is the serialized integer stored in the first
    # char and the first bit in the first char represents the sign
    size_of_val = int(byte_stream[offset] & 0x7F)
    is_negative = bool(byte_stream[offset] & 0x80)
    offset = offset + 1
    end_offset = offset + size_of_val

    # fetch the bytes
    bytes_of_val = byte_stream[offset:end_offset]

    # recover the integer from bytes
    base = 1
    for b in bytes_of_val:
        val += int(b) * base
        base <<= 8
    val = -val if is_negative else val

    return val, end_offset


def serialize_string(val: str):
    return serialize_bytes(val.encode())


def serialize_bytes(val: bytes):
    bytes_in_val = bytearray()

    # append size
    serialized_size = serialize_integer(len(val))
    bytes_in_val.extend(serialized_size)

    # append bytes of string
    bytes_in_val.extend(val)

    return bytes_in_val


def deserialize_string(byte_stream: bytearray, offset=0):
    # deserialize size of string
    size_of_val, offset = deserialize_integer(byte_stream, offset)
    end_offset = size_of_val + offset

    # fetch bytes of string
    bytes_in_val = byte_stream[offset:end_offset]

    # decode string from bytes
    val = bytes_in_val.decode(encoding='utf-8')

    return val, end_offset


def serialize_doc(val: Doc):
    bytes_in_val = bytearray()
    bytes_in_val.extend(serialize_integer(val.doc_id))
    bytes_in_val.extend(serialize_string())
    bytes_in_val.extend(serialize_string(val.content))
    return bytes_in_val


def deserialize_doc(byte_stream: bytearray, offset=0):
    val = Doc()
    val.doc_id, offset = deserialize_integer(byte_stream, offset)
    val.title, offset = deserialize_string(byte_stream, offset)
    val.content, offset = deserialize_string(byte_stream, offset)
    return val, offset
