from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os
import traceback   # → para imprimir el error exacto en los logs

app = Flask(_name_)

# ‼ La clave se lee desde la variable de entorno: OPENAI_API_KEY
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
    # Twilio envía los datos en application/x-www-form-urlencoded → se usa request.values
    incoming_msg = request.values.get("Body", "").strip()
    print("📨 Mensaje recibido:", incoming_msg)

    # Mensaje vacío → no hacemos nada
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
        # Imprimimos el error completo en los logs de Render:
        traceback.print_exc()
        reply_text = "Perdona, hubo un error. Intenta de nuevo en un momento."

    twiml_resp = MessagingResponse()
    twiml_resp.message(reply_text)
    return str(twiml_resp)

if _name_ == "_main_":
    # Render asigna el puerto con la variable PORT; localmente usa 5000
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
