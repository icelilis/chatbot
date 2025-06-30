from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os
import traceback

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

FERMIN_STYLE = """
Responde como Fermin, dueño del proyecto ICELILIS. Tu tono es directo pero amable, con frases como "bendiciones", "claro que sí", "te entiendo". 
No uses lenguaje robótico. Sé natural y paciente.
"""

@app.route("/", methods=["GET"])
def home():
    return "ICELILIS bot activo"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    print("📨 Mensaje recibido:", incoming_msg)

    if not incoming_msg:
        return "OK", 200

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": FERMIN_STYLE},
                {"role": "user", "content": incoming_msg}
            ],
            max_tokens=150,
            temperature=0.7
        )
        reply_text = response.choices[0].message.content.strip()
    except Exception as e:
        traceback.print_exc()
        reply_text = "Perdona, hubo un error. Intenta de nuevo en un momento."

    twiml_resp = MessagingResponse()
    twiml_resp.message(reply_text)
    return str(twiml_resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))