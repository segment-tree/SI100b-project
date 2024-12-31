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

while True:

    response = client.chat.completions.create(
        model="llama3.2",      
        messages=messages,   
    )
    assistant_reply = response.choices[0].message.content
    print(assistant_reply)
    messages.append({"role": "assistant", "content": assistant_reply})


    user_input = input("User input: ")
    if user_input.lower() in ['exit','quit']:#退出聊天
        print("chat ends.")
        break

    messages.append({"role": "user", "content": user_input})


