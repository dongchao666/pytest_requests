import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pytest
import zipfile
from config import readConfig

cur_path = os.path.dirname(os.path.realpath(__file__))

# unittest 使用的方法 弃用
# def add_case(caseName="testcases", rule="test*.py"):
#     '''加载全部的测试用例'''
#
#     # 用例所在文件夹
#     case_path = os.path.join(cur_path, caseName)
#
#     if not os.path.exists(case_path):
#         os.mkdir(case_path)
#     print(f"test testcases path:{case_path}")
#
#     # 定义discover 方法的参数
#     discover = unittest.defaultTestLoader.discover(case_path, pattern=rule, top_level_dir=None)
#
#     print(discover)
#
#     return discover

def zip_file(src_dir):
    zip_name=src_dir+".zip"
    z = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(src_dir):
        fpath = dirpath.replace(src_dir, '')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)

    print('==压缩成功==')

    z.close()

def run_case(reportName="report"):
    """执行所有的测试用例,并把结果写入报告中"""
    now = time.strftime("%Y%m%d%H%M%S")
    report_path = os.path.join(cur_path, reportName)

    # 如果report文件夹不存在的话,就新建一个
    if not os.path.exists(report_path):
        os.mkdir(report_path)

    report_name = now # + "_report.html"
    print(report_name)
    report_file=os.path.join(report_path,report_name)
    # 执行用例
    pytest.main([f'--alluredir={report_file}'])

    # 将数据保存报告
    global output
    output=os.path.join(report_file,"html")
    os.system(f"allure generate {report_file} -o {output} --clean")

    #将报告压缩成zip
    zip_file(output)

# unittest 使用的方法 弃用
# def get_report_file(report_path):
#     '''获取最新的测试报告'''
#     lists = os.listdir(report_path)
#
#     lists.sort(key=lambda fn: os.path.getmtime(os.path.join(report_path, fn)))
#
#     # 找到最新的测试报告
#     lists.reverse()
#     for list in lists:
#         if ".html" in list:
#             report_file = os.path.join(report_path, list)
#             print(f"最新的测试报告:{list}")
#             break
#
#
#     return report_file

# unittest 使用的方法 如果发送pytest的报告的话,需要进行修改
def send_mail(sender, psw, receiver, smtpserver, report_file, port):
    """发送邮件内容"""
    # with open(report_file, "rb") as f:
    #     mail_body = f.read()
    mail_body =f"测试已经完成,完成时间：{time.strftime('%Y/%m/%d %H:%M:%S')}"
    #定义邮件内容
    msg=MIMEMultipart()
    body=MIMEText(mail_body,_subtype="html",_charset="utf-8")
    msg['Subject']=u"自动化测试报告"
    msg['from']=sender
    msg['to']=psw
    msg.attach(body)

    # 添加附件
    att =MIMEText(open(report_file,"rb").read(),"base64","utf-8")
    att['Content-Type']="application/octet-stream"
    att['Content-Disposition'] = 'attachment;filename="report.zip"'
    msg.attach(att)
    try:
        smtp=smtplib.SMTP_SSL(smtpserver,port)
    except Exception as e:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver,port)
    #用户名 密码
    smtp.login(sender,psw)
    smtp.sendmail(sender,receiver,msg.as_string())
    smtp.quit()
    print(f'test report email has send out !')

if __name__ == '__main__':
    # 加载用例
    # all_case=add_case()
    #执行用例
    run_case()
    # 获取最新的测试报告
    # report_path=os.path.join(cur_path,"report")
    # report_file=get_report_file(report_path)

    # 邮箱配置
    sender=readConfig.sender
    psw=readConfig.psw
    smtp_server=readConfig.smtp_server
    port=readConfig.port
    receiver=readConfig.receiver
    send_mail(sender,psw,receiver,smtp_server,f"{output}.zip",port)
