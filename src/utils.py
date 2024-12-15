import base64

def write_data(file_name: str, data: bytes):
    """
    Write data to a file after encoding it to base64.

    Parameters:
    - file_name (str): Path to the file where data will be written.
    - data (bytes): Data to write to the file.
    """
    # Encode data to base64 format
    data = base64.b64encode(data)

    with open(file_name, 'wb') as f:
        f.write(data)

def read_data(file_name: str) -> bytes:
    """
    Read data from a file and decode it from base64.

    Parameters:
    - file_name (str): Path to the file to read from.

    Returns:
    - bytes: Decoded data.
    """
    with open(file_name, 'rb') as f:
        data = f.read()

    # Decode data from base64 format
    return base64.b64decode(data)

def read_data_split(file_name: str) -> list[bytes]:
    """
    Read and split base64-encoded data from a file.

    Parameters:
    - file_name (str): Path to the file to read from.

    Returns:
    - list[bytes]: List of decoded data splits.
    """
    with open(file_name, 'rb') as f:
        # Split data by separator `@`
        data = f.read().split(b'@')

    # Decode each part from base64 format
    return [base64.b64decode(a) for a in data]

def write_data_append(file_name: str, data: bytes):
    """
    Append data to a file after encoding it to base64, with a separator.

    Parameters:
    - file_name (str): Path to the file where data will be appended.
    - data (bytes): Data to append to the file.
    """
    # Encode data to base64 format
    data = base64.b64encode(data)

    with open(file_name, 'ab') as f:
        # Write data with `@` separator
        f.write(b'@' + data)


def print_section(title):
    """Print a formatted section.
    
    Parameters:
    - title (str): Title of the section.
    """
    print()
    print("=" * 50)
    print(f"{title.center(50)}")
    print("=" * 50)
