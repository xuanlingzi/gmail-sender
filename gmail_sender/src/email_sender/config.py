import yaml
import argparse


def load_config_file(config_file_path):
    """从 YAML 配置文件中加载配置"""
    with open(config_file_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def parse_args(config):
    """解析命令行参数并和配置文件进行合并"""
    parser = argparse.ArgumentParser(description="给多个用户发送一对一邮件")
    parser.add_argument('-c', '--config', help="配置文件路径", default='config.yaml')
    parser.add_argument('-s', '--subject', help="邮件标题", default=None)
    parser.add_argument('-b', '--body', help="邮件正文（HTML）", default=None)

    args = parser.parse_args()
    if args.subject is not None:
        config['template']['subject'] = args.subject
    if args.body is not None:
        config['template']['body'] = args.body

    merged_config = config.copy()
    merged_config.update(vars(args))
    return merged_config
