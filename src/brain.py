import google.generativeai as genai
import json
import logging
import re
from config import GEMINI_API_KEY, LOGS_DIR

# 로그(기록) 남기기 설정
logging.basicConfig(filename=LOGS_DIR / 'brain.log', level=logging.INFO)

class BrainEngine:
    def __init__(self):
        # 엔진 시동: 제미나이 연결
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def _clean_json(self, text):
        # AI가 가끔 ```json ... ``` 이런 기호를 붙여서 주는데, 그걸 떼어내는 함수입니다.
        match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        return match.group(1) if match else text

    def generate_vocabulary_data(self, topic, num_words=5):
        # 프롬프트(명령어) 작성
        prompt = f"""
        주제 '{topic}'에 맞는 초급 한국어 단어 {num_words}개를 JSON 데이터로 만들어줘.
        형식 예시: {{ "topic": "{topic}", "words": [ {{ "korean": "사과", "example": "사과가 맛있다.", "image_prompt": "Watercolor illustration of a red apple, white background" }} ] }}
        중요: image_prompt는 그림을 그리기 위해 영어로 써야 하고, 'watercolor style'(수채화) 느낌을 꼭 넣어줘.
        """
        try:
            res = self.model.generate_content(prompt)
            # 텍스트를 파이썬 딕셔너리(데이터)로 변환
            data = json.loads(self._clean_json(res.text))
            return data
        except Exception as e:
            logging.error(f"기획 실패: {e}")
            return None