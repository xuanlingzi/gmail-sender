import base64
import os.path
import time
import main
from email.message import EmailMessage

import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    'https://www.googleapis.com/auth/gmail.compose'
]


def send_email(config, body, to, attachment_list=None) -> bool:
    if config['gmail']['username'] is None or config['gmail']['credential'] is None:
        print("发件人邮箱和密钥JSON文件不能空！")
        return False

    sender = config['gmail']['username']
    credentials_path = config['path']['credential'] + config['gmail']['credential']

    message = EmailMessage()
    message['from'] = 'Your Name <' + sender + '>'
    message['to'] = to
    message['subject'] = config['template']['subject']
    message.set_content(body, subtype='html')
    encode_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    # 添加附件
    if attachment_list:
        for attach in attachment_list:
            try:
                with open(attach["path"], "rb") as f:
                    filename = attach['name']
                    content = f.read()
                    message.add_attachment(content, maintype='application', subtype='pdf', filename=filename)
            except Exception as e:
                print(e)
                return False

    retries = 0
    while retries <= config['application']['retries']:
        try:
            creds = None
            if os.path.exists(credentials_path):
                try:
                    creds = Credentials.from_authorized_user_file(credentials_path)
                except Exception as e:
                    print('原始密钥JSON文件，需要交换Token: %s' % e)
                    creds = None

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(google.auth.transport.requests.Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        credentials_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                with open(credentials_path, 'w') as token:
                    token.write(creds.to_json())

            service = build('gmail', 'v1', credentials=creds)
            send_message = (service.users().messages().send(userId="me", body=encode_message).execute())
            # print(send_message)
            return True

        except HttpError as e:
            print('GMAIL发送邮件错误: %s' % e)
            retries += 1
            if retries > config['application']['retries']:
                print("重试次数已达上限，放弃发送！")
                break
            else:
                print('重试第%d次...' % retries)
                time.sleep(config['application']['interval'])

    return False
