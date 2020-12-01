def cipher():
    L2I = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",range(26)))
    I2L = dict(zip(range(26),"ABCDEFGHIJKLMNOPQRSTUVWXYZ"))

    key = 3
    plaintext = "test"

    # encipher
    ciphertext = ""
    for c in plaintext.upper():
        if c.isalpha(): ciphertext += I2L[ (L2I[c] + key)%26 ]
        else: ciphertext += c

    # decipher
    plaintext2 = ""
    for c in ciphertext.upper():
        if c.isalpha(): plaintext2 += I2L[ (L2I[c] - key)%26 ]
        else: plaintext2 += c

    ciphertext = ciphertext.lower()
    plaintext2 = plaintext2.lower()

    print(ciphertext)
    print(plaintext2)

cipher()
