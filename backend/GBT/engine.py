import os
from typing import List

import openai
from openai import OpenAI

def chat_completion_gbt(prompt: str, args: List):
    try:
        client = OpenAI(
            api_key=os.getenv("OPEN_API_KEY"),
        )
        chat_completion = client.chat.completions.create(model="gpt-4",
                                                       messages=[{"role": "user",
                                                                  "content": f"{prompt}; {args[0]}"}])
        response = chat_completion.choices[0].message.content
        return response
    except Exception as e:
        ...
