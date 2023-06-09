import os
from typing import List

import openai


def chat_completion_gbt(prompt: str, args: List):
    try:
        openai.organization = os.getenv("OPENAI_ORGANIZATION")
        openai.api_key = os.getenv("OPEN_API_KEY")
        # create a chat completion
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-0301",
                                                       messages=[{"role": "user",
                                                                  "content": f"{prompt}; {args[0]}"}])
        response = chat_completion.choices[0].message.content
        return response
    except Exception as e:
        ...
