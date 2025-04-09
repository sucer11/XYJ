from openai import OpenAI
import os
import json

email_content = {
        "Subject": "转发：关于东华大学钓鱼邮件演练的说明—信息化办公室",
        "From": "刘思敏, <220120114@mail.dhu.edu.cn>",
        "Date": "Tue, 5 Nov 2024 05:37:58 +0800 (GMT+08:00)",
        "Content": "x220120114@mail.dhu.edu.cn\n 邮箱：220120114@mail.dhu.edu.cn\n \n\n\n\n---- 转发的邮件 ----\n发件人  admin<admin@mail.dhu.edu.cn> 日期  2024年03月26日 11:03 收件人  220120114@mail.dhu.edu.cn 抄送至   主题  关于东华大学钓鱼邮件演练的说明—信息化办公室  \n\n关 于东华大学钓鱼邮件演练的说明\n 同学：您好！\n我们不幸地通知您：\n由于您在本次学校开展的钓鱼邮件演练中，未能第一时间准确的识别出钓鱼邮件，因此收到了该邮件。演练过程中，不会记录学生的账号密码，此邮件目的旨在警醒各位同学。 \n近年来，钓鱼邮件异常活跃，不法组织利用系统密码过期、系统升级、培训升职、各种优惠等“吸引眼球”的热门内容来吸引用户点击非法链接，窃取学校用户账号密码及重要数据，具有极强的隐蔽性、持续性和危害性。 \n为持续提升广大师生的网络安全意识，今后我校将会不定期开展钓鱼邮件演练。 \n \n信息化办公x室\n2024年3月26日\n如何识别钓鱼邮件及钓鱼网站\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\r\n\r\n 220120114@mail.dhu.edu.cn 邮箱：220120114@mail.dhu.edu.cn ---- 转发的邮件 ---- 发件人 adminadmin@mail.dhu.edu.cn 日期 2024年03月26日 11:03 收件人 220120114@mail.dhu.edu.cn 抄送至 主题 关于东华大学钓鱼邮件演练的说明—信息化办公室 关于东华大学钓鱼邮件演练的说明同学：您好！我们不幸地通知您：由于您在本次学校开展的钓鱼邮件演练中，未能第一时间准确的识别出钓鱼邮件，因此收到了该邮件。演练过程中，不会记录学生的账号密码，此邮件目的旨在警醒各位同学。近年来，钓鱼邮件异常活跃，不法组织利用系统密码过期、系统升级、培训升职、各种优惠等“吸引眼球”的热门内容来吸引用户点击非法链接，窃取学校用户账号密码及重要数据，具有极强的隐蔽性、持续性和危害性。为持续提升广大师生的网络安全意识，今后我校将会不定期开展钓鱼邮件演练。信息化办公室2024年3月26日如何识别钓鱼邮件及钓鱼网站 "
}


class LLM:
    apiToken = 'sk-qlxuepablzgtiwyffvhiagmesatdjwagknrqupykrnvmszji'
    url = "https://api.siliconflow.cn/v1"
    prompt_summary = ""
    prompt_classify = ""

    type_def = {}
    headers = {}

    def __init__(self, user_summary="", user_classify=""):

        current_path = os.path.abspath(__file__)
        current_path = os.path.dirname(current_path)
        parent_path = os.path.dirname(current_path)

        LLM.type_def = json.load(open(f'{parent_path}/rc/type_def.json'))

        LLM.prompt_summary = f"""
        你是一个人工智能邮件处理助手.接下来用户将输入一封邮件,
        邮件格式为JSON格式,包含如下字段: Subject From Date Content.
        综合上述四个字段,在保留邮件关键内容信息的前提下,将邮件内容提炼后简略输出,
        最终输出不用遵循原有格式,不必分点陈述.尽量采用一句话描述事件.
        {user_summary}
        """

        LLM.prompt_classify = f"""
        你是一个人工智能办公邮件处理助手.接下来用户将输入一封邮件,邮件格式为JSON格式,包含如下字段: Subject From Date Content.
        同时,我们对如下几个邮件类型进行定义 {LLM.type_def}, 你需要输出这封邮件所属的类型,只需要输出类型,不要输出其余描述性文本.
        {user_classify}
        """

def query_using_openai( query: str, email: dict) -> str:
        print(query+ json.dumps(email,ensure_ascii=False))
        with OpenAI(api_key=LLM.apiToken, base_url=LLM.url) as client:
            response = client.chat.completions.create(
                model='meta-llama/Meta-Llama-3.1-8B-Instruct',
                messages=[
                    {
                        "role": "user",
                        "content": query+ json.dumps(email,ensure_ascii=False)
                    },
                ],
                stream=False,
                max_tokens=512,
                temperature=0.9,
                top_p=0.7,
                frequency_penalty=0.0,
            )
            return response.choices[0].message.content

if __name__ == "__main__":
    llm = LLM()
    print(query_using_openai(LLM.prompt_summary, email_content))