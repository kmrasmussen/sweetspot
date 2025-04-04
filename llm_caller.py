from openai import OpenAI
import os
from config import *
print('api key openrouter', OPENROUTER_API_KEY)

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENROUTER_API_KEY
)

def get_response(system_prompt, user_prompt, model_name):
  completion = client.chat.completions.create(
    model=model_name,
    temperature=0.5,
    messages=[
      {
        "role": "system",
        "content": system_prompt
      },
      {
        "role": "user",
        "content": user_prompt
      }
    ]
  )

  return completion.choices[0].message.content

if __name__ == "__main__":
  print(get_response("you are a helpful assistant", "what is 2+2?", "openai/gpt-4o-mini"))