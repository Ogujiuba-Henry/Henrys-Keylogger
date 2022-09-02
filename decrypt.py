from cryptography.fernet import Fernet


with open("thekey.key","rb") as thekey:
    key = thekey.read()

with open("log.txt", "rb") as thetest:
    contents = thetest.read()

contents_decrypted =  Fernet(key).decrypt(contents)

with open("log.txt", "wb") as thetest1:
    thetest1.write(contents_decrypted)
