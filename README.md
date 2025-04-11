# 邮差
本程序主要用途是通过smtp给用户发送一对一邮件，支持附件，支持html格式，支持多个收件人，支持多个附件

### 使用方法
python3.10 main.py

### 参数说明
```
-c 配置文件 # 可选 默认文件名 config.yaml
-s 邮件主题 # 可选 默认用配置文件内的标题
-b 邮件正文 # 可选 默认用配置文件内的正文
```

## Gmail API
### 系统要求
1. Python 3.10
2. pip3.10 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib pyyaml

### Gmail API 发送邮件配置方式
1. 登录 https://console.cloud.google.com 开通 Google API
2. 在 Google API 中开通 Gmail API
3. 在凭据中创建 OAuth 2.0 客户端 ID
   1. 选择应用类型为桌面应用
   2. 下载客户端密钥JSON文件，重命名为 credentials.json
   3. 将 credentials.json 放入 credentials 目录内
4. 第一次运行程序时，会自动打开浏览器，登录 Google 帐户，获取授权码
5. 授权成功后系统会自动替换 credentials.json 中的授权码，下次运行程序时将自动使用授权码登录
6. 如果需要更换帐户，只需要删除 credentials.json 文件，重新下载客户端密钥JSON文件，重命名为 credentials.json 即可

#### Gmail SMTP
如果帐户开启了两步验证，需要在两步验证配置内生成一个应用专用密码，然后使用该密码作为SMTP_PASSWORD

### 配置文件说明
```
# 应用程序
application:
  # 应用名称
  name: Postman
  # 版本号
  version: 0.1.0
  # 日志级别
  level: info
  # 是否使用 Gmail API
  gmail: true
  # 间隔时间，单位秒
  interval: 2
  # 重试次数
  retries: 3

# 邮件模版
template:
  # 邮件主题
  subject: '10%OFF for you!'
  # 邮件正文
  body: 10%OFF.html
  # 邮件附件
  attachment: 10%OFF.pdf, 10%OFF.jpg

# 路径
path:
  # 邮件附件
  attachment: ./attachments/
  # 邮件名单
  name: ./emails/
  # 邮件模版
  template: ./templates/
  # Gmail API 凭证
  credential: ./credentials/
  # 日志
  log: ./logs/

# 名单文件
list:
  # 待发件名单
  to: new.txt
  # 已发件名单
  sent: sent.txt
  # 发送失败名单
  failed: failed.txt

# 邮件服务器配置
smtp:
  # 是否使用 SSL
  ssl: false
  # SMTP 服务器
  host: smtp.gmail.com
  # SMTP 端口
  port: 587
  # SMTP 用户名
  username: your.name@gmail.com
  # SMTP 密码
  password: your.password

# Gmail API 凭证
gmail:
  # Gmail 用户名
  username: your.name@gmail.com
  # Gmail API 凭证文件
  credential: credentials.json
```