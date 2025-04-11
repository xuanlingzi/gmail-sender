import time
import os
from .config import load_config_file, parse_args
from .utils.logging_utils import setup_logging
from .utils.file_utils import load_email_list, remove_from_list, read_body_file
from .email.gmail import send_email as gmail_send_email
from .email.smtp import send_email as smtp_send_email


def process_attachments(path, attachments_str):
    """处理附件列表字符串"""
    if attachments_str:
        attachment_list = [{
            "name": attach.strip().split("/")[-1],
            "path": path + attach.strip()
        } for attach in attachments_str.split(',')]
    else:
        attachment_list = []
    return attachment_list


def send_emails(config, html_body):
    """发送邮件"""
    if html_body is None or len(html_body) == 0:
        print("缺少邮件正文！")
        return

    # 从文件中加载电子邮件地址列表
    to_list = load_email_list(config['path']['name'] + config['list']['to'])
    sent_list = load_email_list(config['path']['name'] + config['list']['sent'])
    failed_list = load_email_list(
        config['path']['name'] +
        config['list']['failed']) if config['list']['failed'] else []
    excluded_list = list(set(failed_list) | set(sent_list))
    attachment_list = process_attachments(config['path']['attachment'],
                                          config['template']['attachment'])

    total = len(to_list)
    print("待发送数量：", total)

    for index, to in enumerate(to_list):
        if to in excluded_list:
            print("跳过邮件：", to)
            remove_from_list(config['path']['name'] + config['list']['to'], to)
            continue

        print('正在发送第 %d/%d 封邮件至: %s...' % (index + 1, total, to))
        if config['application']['gmail'] is not None and config['application'][
                'gmail']:
            ok = gmail_send_email(config, html_body, to, attachment_list)
        else:
            ok = smtp_send_email(config, html_body, to, attachment_list)

        if ok:
            print('成功发送邮件至: %s' % to)
            sent_list.append(to)
            with open(config['path']['name'] + config['list']['sent'],
                      'a') as f:
                f.write('\n' + to)
            remove_from_list(config['path']['name'] + config['list']['to'], to)
        else:
            print('发送邮件至 %s 失败！' % to)
            failed_list.append(to)
            if os.path.isfile(config['path']['name'] +
                              config['list']['failed']):
                with open(config['path']['name'] + config['list']['failed'],
                          'a') as f:
                    f.write('\n' + to)
            else:
                with open(config['path']['name'] + config['list']['failed'],
                          'w') as f:
                    f.write(to)

        if index + 1 < total and config['application']['interval'] > 0:
            print('等待%d秒...' % config['application']['interval'])
            time.sleep(config['application']['interval'])

    print('所有邮件发送完毕!')


def main():
    # 加载配置文件
    config = load_config_file('config.yaml')

    # 解析命令行参数并和配置文件进行合并
    config = parse_args(config)

    setup_logging(
        config['path']['log'] + config['application']['level'] + '.log',
        config['application']['level'].upper())

    # 读取邮件正文
    html_body = read_body_file(config['path']['template'] +
                               config['template']['body'])

    # 发送邮件
    send_emails(config, html_body)


if __name__ == '__main__':
    main()
