from cryptography.fernet import Fernet

def encrypt():
    # key = Fernet.generate_key()      || So the key doesn't change everytime I re-run my main file

    with open("thekey.key","rb") as thekey:
        key = thekey.read()

    with open("log.txt", "rb") as thetest:
        contents = thetest.read()

    contents_encrypted =  Fernet(key).encrypt(contents)

    with open("log.txt", "wb") as thetest1:
        thetest1.write(contents_encrypted)

encrypt()

