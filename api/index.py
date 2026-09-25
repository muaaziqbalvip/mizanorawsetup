from flask import Flask, request
import google.generativeai as genai
import requests

app = Flask(__name__)

GEMINI_KEY = "AQ.Ab8RN6JJepno4OaBxbU_OWmi_NLX2mLvqgK2icEW8POqlcJpSg"
WHATSAPP_TOKEN = "EAAQALrGBuZAEBStbZBgNvnc5weCs1fpxtZBi7roMkZAY2Aq5tmr9sKxkJuSUgwkartAfDJoWU75CZBNyMezBYVE7iXgjzfNq4rfasDLkn7UvOxUPwsfnxZB81VZBgn9tAf7mayJVVvHY73oc5AVpLb4U2ZCkLEVK2qY75Huek2TKFrZCJ08Nsl9LaQxuvHq12MgZDZD"
PHONE_ID = "1348689928326141"

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
VERIFY_TOKEN = "kasur123"

@app.route('/api/webhook', methods=['GET', 'POST'])
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return "fail", 403

    if request.method == 'POST':
        data = request.get_json()
        try:
            msg_data = data['entry'][0]['changes'][0]['value']['messages'][0]
            message = msg_data['text']['body']
            from_number = msg_data['from']

            prompt = f"Tum Kasur Brand ke ho, Roman Urdu me 2 line me jawab do. Sawal: {message}"
            ai_reply = model.generate_content(prompt).text

            url = f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages"
            headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
            payload = {
                "messaging_product": "whatsapp",
                "to": from_number,
                "text": {"body": ai_reply}
            }
            requests.post(url, headers=headers, json=payload)
        except:
            pass
        return "OK", 200

# Vercel ke liye zaroori
if __name__ == '__main__':
    app.run()
