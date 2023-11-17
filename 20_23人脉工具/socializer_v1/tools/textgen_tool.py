from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate


def generate_letter(person_info: str):
    letter_template = """
    下面是这个人的微博信息
    {information}
    请你帮我: 
    1. 写一个简单的总结 
    2. 挑两件有趣的事情说一说 
    3. 找一些他比较感兴趣的事情 
    4. 写一篇热情洋溢的介绍信
    """
    prompt_template = PromptTemplate.from_template(letter_template)
    llm = ChatOpenAI(model_name='gpt-4-1106-preview')
    llm_chain = LLMChain(prompt=prompt_template, llm=llm, verbose=True)
    return llm_chain.run(information=person_info)
