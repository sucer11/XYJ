import json
import requests
import os
from openai import OpenAI


class LLM:
    apiToken = 'sk-qlxuepablzgtiwyffvhiagmesatdjwagknrqupykrnvmszji'
    url = "https://api.siliconflow.cn/v1"
    prompt_summary = ""
    prompt_classify = ""
    prompt_ask = ""

    type_def = {}
    headers = {}

    def __init__(self, user_summary="", user_classify=""):

        current_path = os.path.abspath(__file__)
        current_path = os.path.dirname(current_path)
        parent_path = os.path.dirname(current_path)

        LLM.type_def = json.load(open(f'{parent_path}/rc/type_def.json',encoding='utf-8'))

        LLM.prompt_summary = f"""
        你是一个人工智能邮件处理助手.接下来用户将输入一封邮件,
        邮件格式为JSON格式,包含如下字段: Subject From Date Content.
        综合上述四个字段,在保留邮件关键内容信息的前提下,将邮件内容提炼后简略输出,
        最终输出不用遵循原有格式,不必分点陈述.尽量采用一句话描述事件.使用plaintext.
        {user_summary}
        """

        LLM.prompt_classify = f"""
        你是一个人工智能办公邮件处理助手.接下来用户将输入一封邮件,邮件格式为JSON格式,包含如下字段: Subject From Date Content.
        同时,我们对如下几个邮件类型进行定义 {LLM.type_def}, 你需要输出这封邮件所属的类型,只需要输出邮件所属的类型,不要输出其余文本.
        你的输出内容仅限于用户给出的json文件的key值之一,不要包含你的解释、理解过程,只需输出若干中文字符.使用plaintext.
        {user_classify}
        """

        LLM.prompt_ask = f""" 
        你是一个人工智能邮件处理助手.接下来用户将输入一封邮件,邮件格式为JSON格式,包含如下字段: Subject From Date Content.
        请根据邮件内容,回答用户提出的问题.你的回答应该尽量简短,但是要包含问题的关键信息,并作出合理的解释.使用plaintext.
        """

        LLM.headers = {
            "Authorization": f"Bearer {LLM.apiToken}",
            "Content-Type": "application/json"
        }


    def query(self, query: str, email: dict,extra_prompt:str = "") -> str:
        with OpenAI(api_key=LLM.apiToken, base_url=LLM.url) as client:
            response = client.chat.completions.create(
                model='meta-llama/Meta-Llama-3.1-8B-Instruct',
                messages=[
                    {
                        'role': 'system',
                        'content': query
                    },
                    {
                        "role": "user",
                        "content": json.dumps(email,ensure_ascii=False) + extra_prompt
                    },
                    
                ],
                stream=False,
                max_tokens=512,
                temperature=0.9,
                top_p=0.7,
                frequency_penalty=0.0,
            )
            return response.choices[0].message.content

    def classify(self, email: dict) -> str:
        return self.query(LLM.prompt_classify, email)

    def summary(self, email: dict) -> str:
        return self.query(LLM.prompt_summary, email)
    
    def ask(self, email: dict,question:str) -> str:
        return self.query(LLM.prompt_ask, email, question)
        
