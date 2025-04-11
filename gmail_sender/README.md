# Gmail Sender

一个用于批量发送个性化邮件的 Python 工具。

## 功能特点

- 支持 Gmail 和 SMTP 两种发送方式
- 支持 HTML 格式的邮件正文
- 支持附件发送
- 支持批量发送和失败重试
- 可配置发送间隔时间
- 详细的日志记录

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/xuanlingzi/gmail-sender.git
cd gmail-sender
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 配置 `config.yaml` 文件（参考 `examples/config.yaml`）
2. 准备邮件列表文件（`to.txt`）
3. 准备邮件模板（HTML 格式）
4. 运行程序：
```bash
python -m gmail_sender.main
```

## 命令行参数

- `-c, --config`: 配置文件路径（默认：config.yaml）
- `-s, --subject`: 邮件标题
- `-b, --body`: 邮件正文（HTML）文件路径

## 项目结构

```
gmail_sender/
├── src/
│   └── gmail_sender/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── email/
│       │   ├── __init__.py
│       │   ├── gmail.py
│       │   └── smtp.py
│       └── utils/
│           ├── __init__.py
│           ├── file_utils.py
│           └── logging_utils.py
├── tests/
├── docs/
├── examples/
└── requirements.txt
```

## 许可证

MIT License 