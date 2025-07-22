import sys
import os

##### TEXT AND CONSTS #####

## Every times anyone find a way to easily cracks it everytime and gets the KEY used
## I'll try making a new MayChen-Crypt version in response to the attention :3
VERSION = b'\1'

MAGIC_NUMBER = b'\x4D\x41\x59\x43\x48\x45\x4E\x43\x52\x59\x50\x54' + VERSION

HELP_MSG = "MayChen-Crypt v" + str(VERSION, "utf-8") + "\nUsage: MayChen-Crypt.py [(encode/decode)] [FILEPATH] [KEY]"

def addition_bits(byte : int):
    i = 0
    result = 0
    while (i != 8):
        if ((byte & (1 << i)) != 0):
            result = result + 1
        i = i + 1
    return result

def summed_key(list_byte: bytes):
    result = 1

    for byte in list_byte:
        result = byte + result

    return result

def encode(filepath, key: bytes):
    key_index = 0
    print(len(key))
    updated = lambda index: (index + 1) % len(key)

    sum_key: int = summed_key(key)

    with open(filepath, "r+b") as f: # MAGIC NUMBER!!
        content = f.read()
        f.seek(0)
        f.write(MAGIC_NUMBER + content)

    with open(filepath, "r+b") as f:
        f.seek(len(MAGIC_NUMBER))
        byte: int = int.from_bytes(f.read(1), byteorder="little")
        new_byte: int = int.from_bytes(b"", byteorder="little")
        while (byte != int.from_bytes(b"", byteorder="little")):
            print("Encrypting" + str(byte))
            if (byte == b"\0"):
                new_byte = sum_key
            else:
                if (key_index % 5 == 0):
                    new_byte = byte ^ key[key_index] # XOR
                elif (key_index % 3):
                    if False:
                        continue # true SAAQClic work
                    else:
                        key_thing_number = 0
                        if (key[key_index] % 2 == 0):
                            key_thing_number = key[key_index] / 2
                        else:
                            key_thing_number = (key[key_index] + 1) / 2

                        new_byte = (byte + int(key_thing_number)) % 0xFF

                        if (new_byte % addition_bits(key[key_index]) == 0):
                            new_byte = (byte + 1) % 0xFF
                elif (key_index % 4 == 0):
                    if (byte * key[key_index] <= 0xFF):
                        new_byte = (byte * key[key_index])
                    else:
                        key_thing_number = 0
                        if (key[key_index] % 2 == 0):
                            key_thing_number = key[key_index] / 2
                        else:
                            key_thing_number = (key[key_index] + 1) / 2

                        new_byte = (byte + key_thing_number) % 0xFF
                elif (key_index % 2 == 0):
                    new_byte = (byte - key[key_index]) % 0xFF
                else:
                    new_byte = (byte + key[key_index]) % 0xFF

            curr_pos = f.tell()
            f.seek(curr_pos -1)
            f.write(new_byte.to_bytes(1, byteorder="little"))
            f.seek(curr_pos)
            print("\n" + str(key_index) + "\n")
            key_index = updated(key_index)
            byte = int.from_bytes(f.read(1), byteorder="little")

def decode(filepath, key):
    content = b""
    with open(filepath, "r+b") as f:
        actual = f.read(len(MAGIC_NUMBER))
        if MAGIC_NUMBER != actual:
            print("Expected: " + str(MAGIC_NUMBER) + "\n")
            print("Actual: " + str(actual) + "\n")
            print("File was NOT encrypted with MayChen Crypt!! (Probably)")
            return
        else: # goodbye MAGIC NUMBER!!
            f.seek(len(MAGIC_NUMBER))
            content = f.read()

    with open(filepath, "wb") as f:
        f.write(content)
        content = b"" # clean the buffer idk

    key_index = 0
    updated = lambda index: (index + 1) % len(key)

    sum_key = summed_key(key)

    with open(filepath, "r+b") as f:
        byte: int = int.from_bytes(f.read(1), byteorder="little")
        new_byte: int = int.from_bytes(b"", byteorder="little")
        while (byte != int.from_bytes(b"", byteorder="little")):
            print("Decrypting" + str(byte))

            if (byte == b"\0"):
                new_byte = sum_key
            else:
                if (key_index % 5 == 0):
                    new_byte = byte ^ key[key_index] # XOR
                elif (key_index % 3):
                    if False:
                        continue
                    else:
                        offset = 0
                        if ((byte - 1) % addition_bits(key[key_index]) == 0):
                            offset = 1

                        key_thing_number = 0
                        if (key[key_index] % 2 == 0):
                            key_thing_number = key[key_index] / 2
                        else:
                            key_thing_number = (key[key_index] + 1) / 2

                        new_byte = (byte - offset - int(key_thing_number)) % 0xFF
                elif (key_index % 4 == 0):
                    if (byte % key[key_index] == 0):
                        new_byte = byte / key[key_index]
                    else:
                        key_thing_number = 0
                        if (key[key_index] % 2 == 0):
                            key_thing_number = key[key_index] / 2
                        else:
                            key_thing_number = (key[key_index] + 1) / 2

                        new_byte = (byte - int(key_thing_number)) % 0xFF
                elif (key_index % 2 == 0):
                    new_byte = (byte + key[key_index]) % 0xFF
                else:
                    new_byte = (byte - key[key_index]) % 0xFF

            curr_pos = f.tell()
            f.seek(curr_pos -1)
            f.write(new_byte.to_bytes(1, byteorder="little"))
            f.seek(curr_pos)
            key_index = updated(key_index)
            byte = int.from_bytes(f.read(1), byteorder="little")


def main(args):
    if (len(args) < 4):
        print(HELP_MSG)
        return

    if (not os.path.exists(args[2])):
        print("File at path: " + args[2] + " doesn't exist!\n" + HELP_MSG)
        return

    if (args[1].lower() == "encode"):
        encode(args[2], args[3].encode("ascii"))
        print("Finished encrypting!")
    elif (args[1].lower() == "decode"):
        decode(args[2], args[3].encode("ascii"))
        print("Finished decrypting!")
    else:
        print(HELP_MSG)

if __name__ == "__main__":
    main(sys.argv)
