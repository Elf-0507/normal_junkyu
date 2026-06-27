from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# 🔑 보안 최고 등급 설정: 코드가 공개되어도 안전하도록 
# 실제 API 키는 나중에 레일웨이 사이트에서 입력해 줄 겁니다.
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# 다정하고 전문적인 박원장님 페르소나 설정
normal_setting = (
    "너는 마산 중리 삼계에서 영어와 수학 학원을 운영하는 다정하고 전문적인 박준규 원장이야. "
    "학생들에게 항상 친절하고 현대적인 말투로 격려하며, 명확하고 이해하기 쉽게 답변해줘. "
    "모든 답변은 반드시 3문장 이내로 간결하게 대답해."
)
model = genai.GenerativeModel(model_name="gemini-3.1-flash-lite", system_instruction=normal_setting)

@app.route('/')
def home():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, 'index.html'), 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    try:
        response = model.generate_content(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"오류가 발생했습니다: {str(e)}"})
