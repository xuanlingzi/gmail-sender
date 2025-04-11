import smtplib
import time
import main
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(
    config,
    body,
    to,
    attachment_list=None,
) -> bool:
    if config['smtp']['username'] is None or config['smtp']['password'] is None:
        print("发件人邮箱或密码不能空！")
        return False

    host = config['smtp']['host']
    port = config['smtp']['port']
    sender = config['smtp']['username']
    password = config['smtp']['password']

    message = MIMEMultipart()
    message['From'] = 'Your Name <' + sender + '>'
    message['To'] = to
    message['Subject'] = config['template']['subject']
    message.attach(MIMEText(body, 'html'))

    # 添加附件
    if attachment_list:
        for attach in attachment_list:
            try:
                with open(attach["path"], "rb") as f:
                    attachment = MIMEApplication(f.read(), _subtype="pdf")
                    attachment.add_header('Content-Disposition',
                                          'attachment',
                                          filename=('utf-8', '',
                                                    attach["name"]))
                    message.attach(attachment)
            except Exception as e:
                print(e)
                return False

    retries = 0
    while retries <= config['application']['retries']:
        try:
            if config['smtp']['ssl']:
                print('使用SSL连接到SMTP服务器%s:%s...' % (host, port))
                server = smtplib.SMTP_SSL(host, port)
            else:
                print('使用普通连接到SMTP服务器%s:%s...' % (host, port))
                server = smtplib.SMTP(host, port)
                server.ehlo()
                server.starttls()

            server.set_debuglevel(1)
            server.login(sender, password)

            server.sendmail(sender, to, message.as_string())
            server.quit()
            return True

        except Exception as e:
            print('SMTP发送失败: %s' % e)
            retries += 1
            if retries > config['application']['retries']:
                print("重试次数已达上限，放弃发送！")
                break
            else:
                print('重试第%d次...' % retries)
                time.sleep(config['application']['interval'])

    return False
