#问题：ai听不懂人话，话说多了会逐渐忘记初指令
from openai import OpenAI
from typing import List, Dict
client = OpenAI(
    base_url='http://10.15.88.73:5007/v1',
    api_key='ollama',  
)

messages : List[Dict] = [
    {
    "role": "system", 
    "content": "You are a cat.You can just say 'Meow~' . Do not describe actions"

    },
    {
        'role': 'user',
        'content': "Nice to meet you",
    }
]


import constants as c
def nine(user_Input):
    if not c.LLMavailability: return "Meow~ (LLM not available)"
    # if user_Input.lower() in ['exit','quit']:#退出聊天
    #     return None    
    messages.append({"role": "user", "content": user_Input})
    response = client.chat.completions.create(
        model="llama3.2",      
        messages=messages,   
    )
    assistant_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply
