import google.generativeai as genai
import os
from dotenv import load_dotenv

# .env 파일에서 API 키 로드
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("❌ API 키를 찾을 수 없습니다. .env 파일을 확인하세요.")
else:
    genai.configure(api_key=api_key)
    print(f"🔑 현재 키: {api_key[:5]}...로 조회 중")
    
    try:
        print("\n📋 사용 가능한 모델 목록:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"❌ 조회 실패: {e}")