from openai import OpenAI
from typing import List, Dict
client = OpenAI(
    base_url='http://10.15.88.73:5007/v1',
    api_key='ollama',  
)

messages : List[Dict] = [
    {
    "role": "system", 
    "content": "I will give you a number representing the difficulty of a game. You need to return me anumber selected from 1 to 5. \
                The higher the number I give to you , the higher the probability of 5 appearing."
                
    },
    {
        'role': 'user',
        'content': "0",
    }
]

def decision(user_Input):
    messages.append({"role": "user", "content": str(user_Input)+ "return a number, do not say anything else"})
    response = client.chat.completions.create(
        model="llama3.2",      
        messages=messages,   
    )
    assistant_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply

if __name__ == "__main__":
    while(1):
        count = input()
        if count == "quit":break
        print(decision(count))

