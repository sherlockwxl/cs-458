f1 = open("ciphertext1", "r")
ciphertext1 = f1.read()

f2 = open("ciphertext2", "r")
ciphertext2 = f2.read()

ciphertext1_byte = bytearray(ciphertext1)
ciphertext2_byte = bytearray(ciphertext2)

finalSize = 0
if len(ciphertext1_byte) > len(ciphertext2_byte):
    finalSize = len(ciphertext1_byte)
else:
    finalSize = len(ciphertext2_byte)

res = bytearray(finalSize)

for i in range(finalSize):
    res[i] = ciphertext1_byte[i] ^ ciphertext2_byte[i]

f = open("xor", "w")
f.write(res)
f.close()

import binascii

print binascii.hexlify(bytearray(ciphertext1_byte))
print binascii.hexlify(bytearray(ciphertext2_byte))
print binascii.hexlify((res))