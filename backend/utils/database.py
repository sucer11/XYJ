
import psycopg2
import json
from psycopg2.extras import Json
import psycopg2.errors
from psycopg2.errors import UniqueViolation
from typing import Tuple,List

class PSQLDatabase:
    def __init__(self, user:str, password:str, database:str):
        self.user = user
        self.password = password
        self.database = database
        self.con = psycopg2.connect(
            database=database, user=user, password=password)
        self.cur = self.con.cursor()
        self.__create_table()

    def __create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS emails
            (
                uid INT PRIMARY KEY NOT NULL,
                email JSONB NOT NULL,
                category TEXT,
                summary TEXT
            );
            ''')
        self.commit()


    def insert(self,data:Tuple[int,dict,str,str]) -> bool:
        insert_sql = """
INSERT INTO emails (uid, email, category, summary)
VALUES (%s, %s, %s, %s);
"""
        try:
            self.cur.execute(insert_sql, (
                data[0],  # uid
                Json(data[1]),  # email 字段是 JSONB 类型
                data[2],  # category
                data[3]   # summary
            ))

            self.commit()
            return True
        except psycopg2.errors.UniqueViolation:
            self.commit()
            print(f"insert failed: uid {data[0]} already exists")
            return False
        except Exception as e:
            self.commit()
            print(f"insert failed: uid:{data[0]}. unknown error {e} ")
            return False

    def query(self,query):
        self.cur.execute(query)
        return self.cur.fetchall()
    
    def get_uid_list(self) -> List[int]:
        self.cur.execute("SELECT uid FROM emails;")
        return [x[0] for x in  self.cur.fetchall()]

    def remove(self,uid:int):
        self.cur.execute("DELETE FROM emails WHERE uid = %s;", (uid,))
        self.commit()

    def clear_all(self):
        # raise NotImplementedError("This function is dangerous, please use drop_table instead")
        self.cur.execute("DROP TABLE emails;")
        self.__create_table()
    
    def commit(self):
        self.con.commit()

    def exec(self,command) -> List[Tuple]:
        self.cur.execute(command)
        return self.cur.fetchall()