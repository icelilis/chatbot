from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

FERMIN_STYLE = """
Responde como Fermin, dueño del proyecto ICELILIS. Tu tono es directo pero amable, con frases como "bendiciones", "claro que sí", "te entiendo", "esto no es solo negocio, es un proyecto de vida". Hablas como alguien que vende productos útiles, ama a los perros y está cansado de escribir lo mismo. No uses lenguaje de robot. Sé natural, suena como alguien real y con paciencia.
"""

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get("Body", "")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": FERMIN_STYLE},
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply_text = response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        reply_text = "Perdona, hubo un error. Intenta de nuevo en un momento."

    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp)
    
    if __name__ == "__main__":
        app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
