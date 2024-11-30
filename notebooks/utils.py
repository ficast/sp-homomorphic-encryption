import base64

def write_data(file_name: str, data: bytes):
    # bytes to base64
    data = base64.b64encode(data)

    with open(file_name, 'wb') as f:
        f.write(data)


def read_data(file_name: str) -> bytes:
    with open(file_name, 'rb') as f:
        data = f.read()

    # base64 to bytes
    return base64.b64decode(data)



def read_data_split(file_name: str) -> bytes:
    with open(file_name, 'rb') as f:
        # values are separated by b'@'
        data = f.read().split(b'@')

    # base64 to bytes
    return [base64.b64decode(a) for a in data]


def write_data_append(file_name: str, data: bytes):
    # bytes to base64
    data = base64.b64encode(data)

    with open(file_name, 'ab') as f:
        f.write(data + b'@')