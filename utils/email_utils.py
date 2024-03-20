import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

MAIL_USER = os.getenv('MAIL_USER', 'mrzihantang@163.com')
MAIL_PASS = os.getenv('MAIL_PASS', 'RVDRKOJEJNFUMKWK')


def send_mail_163(recv, title, content, file_path):
    send_mail(MAIL_USER, MAIL_PASS, recv=recv, title=title, content=content, file_path=file_path)


def send_mail(username, passwd, recv, title, content, mail_host='smtp.163.com', port=25, file_path=None):
    """
    发送邮件，默认使用163smtp

    :param username: 邮箱账号 xx@163.com
    :param passwd: 邮箱密码
    :param recv: 邮箱接收人地址，多个账号以逗号隔开
    :param title: 邮件标题
    :param content: 邮件内容
    :param mail_host: 邮箱服务器
    :param port: 端口号
    :param file_path: 文件路径
    :return:
    """
    if file_path:
        msg = MIMEMultipart()

        # 构建正文
        part_text = MIMEText(content)
        msg.attach(part_text)  # 把正文加到邮件体里面去

        # 构建邮件附件
        part_attach1 = MIMEApplication(open(file_path, 'rb').read())  # 打开附件
        part_attach1.add_header('Content-Disposition', 'attachment', filename=file_path)  # 为附件命名
        msg.attach(part_attach1)  # 添加附件
    else:
        msg = MIMEText(content)  # 邮件内容
    msg['Subject'] = title  # 邮件主题
    msg['From'] = username  # 发送者账号
    msg['To'] = recv  # 接收者账号列表
    smtp = smtplib.SMTP(mail_host, port=port)
    smtp.login(username, passwd)  # 登录
    smtp.sendmail(username, recv, msg.as_string())
    smtp.quit()


if __name__ == '__main__':
    recv = "zhtangsh@163.com"
    title = "测试邮件"
    content = "测试邮件内容"
    file_path = "../cb_price_flat.xlsx"
    send_mail_163(recv, title, content, file_path)
