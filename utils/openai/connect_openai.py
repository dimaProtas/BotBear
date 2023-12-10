# import os
import g4f
import asyncio
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()


# client = OpenAI(
#                 api_key=str(os.environ.get("CHAT_GPT_KEY")),
#                 # base_url="https://api.proxyapi.ru/openai/v1",)
#                 base_url="https://api.openai.com/v1",)

# g4f.debug.logging = True # Логирование


async def openai_send(message_text):
  completion = await g4f.ChatCompletion.create_async(
    model=g4f.models.gpt_35_turbo,
    messages=message_text,
  )

  return completion


def generate_img(message_image):
  response = g4f.ChatCompletion.create(
    model="dall-e-3",
    prompt=message_image,
    size="1024x1024",
    quality="standard",
    n=1,
  )
  if response.data[0].url:
    return response.data[0].url
  else:
    return 'Ой, что-то пошло не так!'
