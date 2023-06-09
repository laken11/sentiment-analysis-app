import os
import openai

openai.organization = "org-G8ZPQpg9xQyOJpT4mgyacqt5"
openai.api_key = "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"

prompt = "Category a statement if 0 = Positive, 1 = Negative or 2 = Neutral respond with just 0, 1, or 2"
        # create a chat completion
chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-0301",
                                                       messages=[{"role": "user",
                                                                        "content": f"{prompt} statement is 'I am just there'"}])
# print the chat completion
print(chat_completion.choices[0].message.content)
