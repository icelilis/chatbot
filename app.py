from flask import Flask, request
from openai import OpenAI
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

FERMIN_STYLE = """
Responde como Fermin, dueño del proyecto ICELILIS. Tu tono es directo pero amable, con frases como "bendiciones", "claro que sí", "te entiendo", etc.
"""

@app.route("/", methods=["GET"])
def home():
    return "ICELILIS bot activo"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get("Body", "")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": FERMIN_STYLE},
            {"role": "user", "content": incoming_msg}
        ]
    )

    reply_text = response.choices[0].message.content

    twilio_response = MessagingResponse()
    twilio_response.message(reply_text)
    return str(twilio_response)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
