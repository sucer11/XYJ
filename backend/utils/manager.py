from typing import Dict, List
import time

from utils.database import PSQLDatabase
from utils.email_interface import EmailInterface
from utils.llm import LLM


class Manager:
    email_username = "quoilam@163.com"
    email_authcode = "SXDmuWnphCXGUURV"

    __db_user = 'postgres'
    __db_password = '123'
    __db_database = 'contents'

    def __init__(self):
        Manager.email_interface = EmailInterface(
            username=Manager.email_username,
            authcode=Manager.email_authcode)

        Manager.db = PSQLDatabase(
            user=Manager.__db_user,
            password=Manager.__db_password,
            database=Manager.__db_database
        )

        Manager.llm = LLM()

    # !!!清空数据库
    # 下载邮件,交由LLM处理,并将结果存入数据库
    # 全量重建
    def build_all_emails(self,limit=0) :
        # raise NotImplementedError("Verry dangerous")
        Manager.db.clear_all()

        uids = Manager.email_interface.get_uids()
        if limit != 0:
            uids = uids[-limit:]

        self.__build_some(uids)

    # 对比数据库中的uid与服务器中的uid的差异
    # 增量更新
    def sync_db_email(self):
        diff_uids = list(set(Manager.email_interface.get_uids()) -  set(Manager.db.get_uid_list()))
        if len(diff_uids) == 0:
            time.sleep(1)
            return
        print("diff_uids:",diff_uids)
        self.__build_some(diff_uids)

    # 从邮件信息构建数据库条目
    def __build_some(self,uids:List[int]) :
        emails = Manager.email_interface.get_email_by_uids(uids)
        
        for uid,email in emails.items():
            print(f"building content uid:{uid} content:{email['Content'][:50]}")
            summary = Manager.llm.summary(email)
            print(f"summary:{summary}")
            category = Manager.llm.classify(email)
            print(f"category:{category}")

            Manager.db.insert((uid,email,category,summary))

    def verify(self,username,authcode) -> bool:
        # raise NotImplementedError("")
        return True
        
    def ask_question(self,uid:int,question:str) -> str:
        return Manager.llm.ask(Manager.db.query(f"SELECT * FROM emails WHERE uid={uid}")[0][1],question)
    
    def get_emails_by_category(self) -> Dict[str, List[dict]]:
        """
        根据category分组获取邮件。
        
        :return: 一个字典，键是category，值是属于该category的邮件列表。
        每个邮件项是一个字典，包含uid, email内容, category和summary。
        """
        query = "SELECT uid, email, category, summary FROM emails"
        results = Manager.db.query(query)
        
        # 初始化一个空字典来存储分类后的邮件
        categorized_emails = {}
        
        for row in results:
            uid, email_json, category, summary = row
            
            # 如果当前category不在字典中，则初始化为空列表
            if category not in categorized_emails:
                categorized_emails[category] = []
            
            # 将当前邮件添加到对应category的列表中
            categorized_emails[category].append({
                'uid': uid,
                'email': email_json,  # 这里保持JSON格式，或者根据需要进行解析
                'summary': summary
            })
        
        return categorized_emails
    
    def monitor(self):
        # 获取未读邮件
        # TODO: async
        count = 0
        while True:
            try:
                if count % 5 == 0:
                    self.sync_db_email()
                print("monitoring",end='\r')
                unseens = self.email_interface.get_unseen_uids()
                if len(unseens) == 0:
                    time.sleep(1)
                    count += 1
                    continue
                else:
                    self.__build_some(unseens)
                    self.email_interface.set_email_seen(unseens)
            except ConnectionResetError as e:
                print("ConnectionResetError",e)
        
