def encrypt(plain_text, key, alphabet):
    # Variant Beaufort cipher - A variant of Vigenere Cipher : encryption

    cipher_text = ""
    key_index = 0

    for char in plain_text:
        if char in alphabet:
            shift = alphabet.index(key[key_index % len(key)])
            cipher_text += alphabet[(alphabet.index(char) - shift) % len(alphabet)]
            key_index += 1
        else:
            cipher_text += char

    return cipher_text


def decrypt(cipher_text, key, alphabet):
    # Variant Beaufort cipher - A variant of Vigenere Cipher : decryption

    plain_text = ""
    key_index = 0

    for char in cipher_text:
        if char in alphabet:
            shift = alphabet.index(key[key_index % len(key)])
            plain_text += alphabet[(alphabet.index(char) + shift) % len(alphabet)]
            key_index += 1
        else:
            plain_text += char

    return plain_text
