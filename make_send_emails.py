import os
import json
import logging
from dotenv import load_dotenv

import resend
import openai

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
resend.api_key = os.getenv("RESEND_API_KEY")

try:
    openai_client = openai.OpenAI()
except openai.OpenAIError as e:
    logging.error(f"OpenAI client creation failed with error: {e}")

# chat with chat gpt
def chat_w_chat_gpt(message: str) -> str:
    try:
        openai_response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f"{message}"}
            ]
        )
        response_content = openai_response.choices[0].message.to_dict()
        return response_content['content']
    except Exception as e:
        logging.info(f"Error chatting with chatGPT: {e}")

# create email content TODO: email html
def create_email(user_data: dict, prompt: str) -> str: 
    first_name = user_data["first_name"]

    response = chat_w_chat_gpt(prompt)
    return response

# sends email to email in data using resend
def send_email(emails: list[str], content: str) -> None:
    params: resend.Emails.SendParams = {
        "from": "dev test <onboarding@resend.dev>",
        "to": emails,
        "subject": "hello",
        "html": content,
    }

    try:
        email = resend.Emails.send(params)
        logging.info("Success! Email sent.")
    except Exception as e:
        logging.error(f"Email failed with error: {e}")

# entry point, good for cloud deploys or idk for fun
def handler():
    with open('data.json', 'r') as file:
        user_data = json.load(file)
    
    prompt = f"tell me hello (my name is {user_data['first_name']}) and write me a cool motivational quote."

    email_content = create_email(user_data, prompt)
    send_email([user_data["email"]], email_content)
    
handler()