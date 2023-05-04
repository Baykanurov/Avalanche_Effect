from typing import Optional
from pathlib import Path

from .hash import Hash


class Manager:
    def __init__(self, file: Optional[str], text: Optional[str], output: Optional[str]):
        self._file = file,
        self._text = text,
        self._output = output

    def write_file(self, result: str):
        with open(Path(self._output), 'w') as file:
            file.write(result)
        print(f'Result write in file: {self._output}')

    def read_file(self) -> bytes:
        try:
            with open(Path(self._file[0] or "."), 'r') as file:
                data = file.read().encode()
            return data
        except FileNotFoundError as error:
            raise error

    @staticmethod
    def get_hash(data) -> str:
        hash_client = Hash()
        original_hash = hash_client.get_original_hash(data=data)
        modified_hash, num_bits_changed = hash_client.modified_hash(data=data)
        format_original_hash = " ".join([format(x, "02x") for x in original_hash])
        format_modified_hash = " ".join([format(x, "02x") for x in modified_hash])
        result = f'Original hash: {format_original_hash}\n' \
                 f'Modified hash: {format_modified_hash}\n' \
                 f'Number of changed bits: {num_bits_changed}\n'
        print(result)
        return result
