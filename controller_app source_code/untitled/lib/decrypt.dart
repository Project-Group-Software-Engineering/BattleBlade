String decrypt(String cipherText, String key, String alphabet) {
  // Variant Beaufort cipher - A variant of Vigenere Cipher : decryption

  String plainText = "";
  int keyIndex = 0;

  for (int i = 0; i < cipherText.length; i++) {
    String char = cipherText[i];
    if (alphabet.contains(char)) {
      int shift = alphabet.indexOf(key[keyIndex % key.length]);
      int charIndex = alphabet.indexOf(char);
      int newIndex = (charIndex + shift) % alphabet.length;
      plainText += alphabet[newIndex];
      keyIndex++;
    } else {
      plainText += char;
    }
  }

  return plainText;
}
