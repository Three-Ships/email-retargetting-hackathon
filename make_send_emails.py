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

# create email content
def create_email(user_data: dict, prompt: str) -> str: 
    first_name = user_data["first_name"]
    response = chat_w_chat_gpt(prompt)
    
    html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Sorry we didn't help you!</title>
        </head>
        <body>
            <h1>Sorry we didn't help you!</h1>
            <h3>{response}</h3>
            <a href="https://three-ships.github.io/email-retargetting-hackathon/?first_name={first_name}" target="_blank">
            <button style="font-size: 18px; padding: 15px 30px; border-radius: 8px; border: none; background-color: #4CAF50; color: white;">Reignite🔥</button></a>
            <p style="position: fixed; bottom: 10px; width: 100%; text-align: center;">If you are not interested in having your house fixed, you can ignore and delete this email.</p>
        </body>
        </html>
    """
    
    return html_template

# sends email to email in data using resend
def send_email(emails: list[str], content: str) -> None:
    params: resend.Emails.SendParams = {
        "from": "Reignite <onboarding@resend.dev>",
        "to": emails,
        "subject": "Sorry we didn't help you!",
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
    
    prompt = f"""
    write me three sentences of an email to a consumer briefly apologizing for not connecting the user with a service provider, and explaining that we care. 
    start with "Hello, {user_data["first_name"]}!"
    include the sentence "click below to explore more providers!" at the end. 
    only return the three sentences with no other formatting or greeting.
    """
    
    email_content = create_email(user_data, prompt)
    send_email([user_data["email"]], email_content)
    
handler()