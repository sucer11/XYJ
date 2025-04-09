
from email.header import decode_header
import email.message
from email.message import Message
import html2text
import re
from typing import List

from imapclient import IMAPClient


class EmailInterface:
    host = "imap.163.com"

    class __Email:
        def __init__(self):
            self.mail = None

        def __enter__(self):
            self.mail = IMAPClient(EmailInterface.host, port=993, ssl=True)
            self.mail.login(EmailInterface.username, EmailInterface.authcode)
            self.mail.id_({
                'name': 'myname',
                'version': '1.0.0',
                'vendor': 'myclient',
                'support-email': 'testmail@test.com',
                "contact": "XXXX@163.com",
            })
            self.mail.select_folder('INBOX')
            return self.mail

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.mail.logout()



    def __init__(self, username, authcode):
        EmailInterface.username = username
        EmailInterface.authcode = authcode

    # 检查数据库中最新的uid与服务器中最新的uid是否一致
    # 如果不一致则将新的邮件存入数据库
    def rebuild_index(self):

        pass

    # 将邮件bytes数据解码,并返回json格式的邮件内容
    def __get_content_json(self,content: bytes) -> dict:
        def __process_mime(mimestr: str) -> str:
            return ",".join([
                seq.decode(codec) if codec else  # 如果有编码信息则使用编码信息解码
                seq.decode('utf-8') if isinstance(seq,bytes) else  # 如果是bytes则直接解码
                seq  # 否则直接返回
                for seq, codec in decode_header(mimestr)
            ])

        def __get_maincontent(message: Message) -> str:
            res = ""
            if message.is_multipart():
                for part in message.walk():
                    content_type = part.get_content_type()

                    # UnicodeDecodeError
                    try:
                        if content_type == 'text/plain':  # 只提取纯文本正文
                            res += part.get_payload(decode=True).decode('utf-8')
                        elif content_type == 'text/html':  # 提取html正文
                            # html_text = part.get_payload(decode=True).decode('utf-8')
                            # html_text = re.sub(
                            #     "<style([\\s\\S]*?)</style>|<[^>]+>|[\\r\\n]+|&[a-z]+;", "", html_text)
                            # html_text = re.sub("[ ]{2,}", " ", html_text)
                            # # 正则解释
                            # # <style\\b[^>]*>(.*?)</style> 匹配style标签
                            # # <[^>]+> 匹配所有html标签
                            # # \\r\\n 匹配换行
                            # # &[a-z]+; 匹配html转义字符 如 &nbsp;
                            # # [ ]{2,} 匹配连续两个以上的空格
                            html_text = part.get_payload(decode=True).decode('utf-8')
                    # 使用html2text将HTML转换为Markdown格式的纯文本
                            converter = html2text.HTML2Text()
                            converter.ignore_links = True
                    # 转换后的文本会较好地保留原始的换行和段落格式
                            res += converter.handle(html_text)

                            # res += html_text
                        else:
                            return message.get_payload(decode=True).decode('utf-8')
                    except (UnicodeDecodeError, AttributeError):
                        continue
            return res

        res = {}
        email_message = email.message_from_bytes(content)

        for key in ['Subject', 'From', 'Date']:
            res[key] = __process_mime(email_message[key])
        res['Content'] = __get_maincontent(email_message)
        return res
    
    def get_uids(self) -> List[int]:
        with self.__Email() as mail:
            res = mail.search("ALL")
        return res
    
    # 按uid获取邮件
    def get_email_by_uids(self, uids: List[int]) -> dict[int,dict]:

        with self.__Email() as mail:
            letter = mail.fetch(uids, ['BODY[]'])

        res:dict[int,dict] = {}  # uid -> content
        for uid in uids:
            content = self.__get_content_json(letter[uid][b'BODY[]'])
            res[uid] = content
        return res
    
    def get_unseen_uids(self) -> List[int]:
        with self.__Email() as mail:
            res = mail.search("UNSEEN")
        return res
    
    def set_email_seen(self,uids:List[int]):
        with self.__Email() as mail:
            mail.set_flags(uids, [b'\\Seen'])