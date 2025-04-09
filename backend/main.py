import subprocess
import threading
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from utils.manager import Manager

app = None
manager = None

# if __name__=="__main__":
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
manager = Manager()

# new thread running manager.monitor()
t = threading.Thread(target=manager.monitor)
t.start()




@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/db_log")
def read_db_log():
    # 使用tail命令获取最后10行
    result = subprocess.run(['tail', '-n', '10', 'db_log'], stdout=subprocess.PIPE, text=True, check=True)
    return "\n".join(result.stdout.splitlines())

@app.get("/last_email")
def read_last_email(limit: int = 10, offset: int = 0):
    query = f"SELECT * FROM emails ORDER BY uid DESC LIMIT {limit} OFFSET {offset}"
    res = manager.db.query(query) 
    return res

@app.get("/email/{uid}")
def get_email_by_uid(uid:int):
    return manager.db.query(f"SELECT * FROM emails WHERE uid={uid}")


@app.get("/get_categories")
def get_categories():
    with open("rc/type_def.json",'r',encoding='utf-8') as fp:
        return json.load(fp)
    
@app.get("/email/category/{category}")
def get_email_by_category(category:str):
    return manager.db.query(f"SELECT * FROM emails WHERE category={category}")
    
@app.post("/set_categories")
def set_categories(categories:dict):
    
    with open("rc/type_def.json",'w',encoding='utf-8') as fp:
        json.dump(categories,fp,ensure_ascii=False)
    return "success"

@app.get("/email_count")
def email_count():
    return len(manager.email_interface.get_uids())

@app.post("/rebuild_all")
def rebuild_all():
    manager.build_all_emails()
    return "success"


@app.get("/login")
def login(username='',authcode=''):
    return manager.verify(username,authcode)


@app.get("/ask")
def ask(uid:int,question:str):
    return manager.ask_question(uid,question)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=13271)