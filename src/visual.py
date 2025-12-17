# src/visual.py
import time
import logging
from config import *

# [최종 수정] grep으로 찾아낸 '진짜 주소' 2곳을 정확히 입력했습니다.
# 1. Flux1 모델 위치
from mflux.models.flux.variants.txt2img.flux import Flux1
# 2. Config 설정 위치
from mflux.models.common.config.config import Config

logging.basicConfig(filename=LOGS_DIR / 'visual.log', level=logging.INFO)

class VisualEngine:
    def __init__(self):
        self.flux = None

    def load_model(self):
        if self.flux:
            return

        print("⏳ Apple MLX 엔진 가동 (Path Fixed)")
        try:
            # quantize=4: M1 16GB 맥북 생존 필수 옵션
            self.flux = Flux1.from_alias(
                alias="schnell", 
                quantize=4
            )
            print("✅ 모델 로드 성공! (모든 주소 확인 완료)")
        except Exception as e:
            print(f"❌ 모델 로드 실패: {e}")
            logging.error(f"모델 로드 에러: {e}")
            raise e

    def generate_image(self, prompt, path):
        self.load_model()
        try:
            print(f"🎨 이미지 생성 시작: {prompt[:30]}...")
            
            # MLX 방식 이미지 생성
            image = self.flux.generate_image(
                seed=int(time.time()),
                prompt=prompt,
                config=Config(
                    num_inference_steps=2, # Schnell 모델은 2스텝 (빠름)
                    height=IMAGE_SIZE,
                    width=IMAGE_SIZE,
                )
            )
            
            # 저장
            image.save(path=path)
            print(f"✨ 저장 완료: {path}")
            return str(path)

        except Exception as e:
            logging.error(f"이미지 생성 실패: {e}")
            print(f"❌ 생성 실패: {e}")
            return None
        
    def unload_model(self):
        self.flux = None