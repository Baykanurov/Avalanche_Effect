class SHA256Constant:
    def __init__(self):
        # Начальные хэш-значения
        # (первые 32 бита дробных частей квадратных корней из первых 8 простых чисел)
        self._initial_hash_values = [
            0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
            0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
        ]
        # Константы
        # (первые 32 бита дробных частей кубических корней первых 64 простых чисел)
        self._constants = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
            0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
            0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
            0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
            0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
            0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
            0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
            0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
            0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]


class Hash(SHA256Constant):

    def __init__(self):
        super().__init__()

    def get_original_hash(self, data: bytes) -> bytes:
        return self._modified_hash(data)

    def modified_hash(self, data: bytes) -> (bytes, int):
        num_bits_changed = 0
        modified_hash = bytes
        # Изменяет 1 бит в начале, середине и конце исходного сообщения
        for i in [0, len(data) // 2, len(data) - 1] or []:
            modified_msg = bytearray(data)
            byte_index = i // 8
            bit_index = i % 8
            modified_msg[byte_index] ^= (1 << (7 - bit_index))
            modified_hash = self._modified_hash(modified_msg)
            num_bits_changed += 1

        return modified_hash, num_bits_changed

    def _modified_hash(self, data: bytes) -> bytes:
        return self._big_endian(self._process_chunk(self._pre_processing(data)))

    def _process_chunk(self, data: bytes) -> list:
        # Разбивает сообщение на 512-битные фрагменты
        chunks = [data[i:i + 64] for i in range(0, len(data), 64)]
        modified_initial_hash_values = self._initial_hash_values

        for chunk in chunks:
            zero_word_64 = [0] * 64

            for i in range(16):
                zero_word_64[i] = int.from_bytes(chunk[i * 4:i * 4 + 4], byteorder='big')

            for i in range(16, 64):
                s0 = self._rotate_right(zero_word_64[i - 15], 7) ^ self._rotate_right(zero_word_64[i - 15], 18) ^ (zero_word_64[i - 15] >> 3)
                s1 = self._rotate_right(zero_word_64[i - 2], 17) ^ self._rotate_right(zero_word_64[i - 2], 19) ^ (zero_word_64[i - 2] >> 10)

                zero_word_64[i] = (zero_word_64[i - 16] + s0 + zero_word_64[
                    i - 7] + s1) & 0xFFFFFFFF

            h0, h1, h2, h3, h4, h5, h6, h7 = modified_initial_hash_values

            # Compression function main loop
            for i in range(64):
                s1 = self._rotate_right(h4, 6) ^ self._rotate_right(h4, 11) ^ self._rotate_right(h4, 25)
                ch = (h4 & h5) ^ (~h4 & h6)
                temp1 = (h7 + s1 + ch + self._constants[i] + zero_word_64[i]) & 0xFFFFFFFF

                s0 = self._rotate_right(h0, 2) ^ self._rotate_right(h0, 13) ^ self._rotate_right(h0, 22)
                maj = (h0 & h1) ^ (h0 & h2) ^ (h1 & h2)
                temp2 = (s0 + maj) & 0xFFFFFFFF

                h7 = h6
                h6 = h5
                h5 = h4
                h4 = (h3 + temp1) & 0xFFFFFFFF
                h3 = h2
                h2 = h1
                h1 = h0
                h0 = (temp1 + temp2) & 0xFFFFFFFF

            # Add the compressed chunk to the current hash value
            modified_initial_hash_values[0] = (modified_initial_hash_values[0] + h0) & 0xFFFFFFFF
            modified_initial_hash_values[1] = (modified_initial_hash_values[1] + h1) & 0xFFFFFFFF
            modified_initial_hash_values[2] = (modified_initial_hash_values[2] + h2) & 0xFFFFFFFF
            modified_initial_hash_values[3] = (modified_initial_hash_values[3] + h3) & 0xFFFFFFFF
            modified_initial_hash_values[4] = (modified_initial_hash_values[4] + h4) & 0xFFFFFFFF
            modified_initial_hash_values[5] = (modified_initial_hash_values[5] + h5) & 0xFFFFFFFF
            modified_initial_hash_values[6] = (modified_initial_hash_values[6] + h6) & 0xFFFFFFFF
            modified_initial_hash_values[7] = (modified_initial_hash_values[7] + h7) & 0xFFFFFFFF

        return modified_initial_hash_values

    @staticmethod
    def _big_endian(initial_hash_values: list) -> bytes:
        digest = (initial_hash_values[0].to_bytes(4, byteorder='big') +
                  initial_hash_values[1].to_bytes(4, byteorder='big') +
                  initial_hash_values[2].to_bytes(4, byteorder='big') +
                  initial_hash_values[3].to_bytes(4, byteorder='big') +
                  initial_hash_values[4].to_bytes(4, byteorder='big') +
                  initial_hash_values[5].to_bytes(4, byteorder='big') +
                  initial_hash_values[6].to_bytes(4, byteorder='big') +
                  initial_hash_values[7].to_bytes(4, byteorder='big'))

        return digest

    @staticmethod
    def _pre_processing(data: bytes) -> bytes:
        size = len(data) * 8  # Размер сообщения в битах
        data += b'\x80'  # Добавить 1 бита после сообщения

        while (len(data) * 8) % 512 != 448:
            data += b'\x00'

        # Добавляет размер сообщения в битах в виде
        # 64-разрядного целого числа с большим порядковым номером
        data += size.to_bytes(8, byteorder='big')

        return data

    @staticmethod
    def _rotate_right(number, count):
        # Развернуть число вправо на count бит (0 <= count < 32)
        return ((number >> count) | (number << (32 - count))) & 0xFFFFFFFF
