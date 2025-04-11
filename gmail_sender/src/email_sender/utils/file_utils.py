import os


def load_email_list(email_list_file):
    """从文件中加载电子邮件地址列表"""
    if not os.path.isfile(email_list_file):
        return []

    with open(email_list_file, 'r') as f:
        email_list = [email.strip() for email in f.readlines()]

    return email_list


def remove_from_list(email_list_file, to):
    """从列表中移除指定的电子邮件地址"""
    if os.path.isfile(email_list_file):
        with open(email_list_file, 'r') as f:
            email_list = f.readlines()

        email_list = [
            email.strip() for email in email_list if email.strip() != to
        ]

        with open(email_list_file, 'w') as f:
            f.writelines('\n'.join(email_list))
    else:
        with open(email_list_file, 'w') as f:
            pass


def read_body_file(body_path):
    """读取邮件正文文件"""
    with open(body_path, 'r') as f:
        html_body = f.read()
    return html_body
