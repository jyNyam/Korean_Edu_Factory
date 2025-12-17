import torch
from diffusers import FluxPipeline
import logging
import gc
from config import *

logging.basicConfig(filename=LOGS_DIR / 'visual.log', level=logging.INFO)

class VisualEngine:
    def __init__(self):
        self.pipe = None 

    def load_model(self):
        # 모델이 없을 때만 로드 (최초 1회만 실행됨 -> 지연 시간 제거)
        if not self.pipe:
            self.pipe = FluxPipeline.from_pretrained(
                FLUX_MODEL, 
                torch_dtype=torch.bfloat16, 
                cache_dir=MODELS_DIR
            )
            # [핵심] CPU Offloading: 모델을 끄지 않고 RAM으로 내려둠 (속도 빠름 + 메모리 절약)
            self.pipe.enable_model_cpu_offload()

    def generate_image(self, prompt, path):
        self.load_model()
        try:
            # 이미지 생성
            img = self.pipe(
                prompt, 
                height=IMAGE_SIZE, 
                width=IMAGE_SIZE, 
                num_inference_steps=4, 
                guidance_scale=0.0
            ).images[0]
            img.save(path)
            
            # [강화된 청소] 이미지 객체만 삭제하여 스왑 방지
            del img
            gc.collect()
            if torch.backends.mps.is_available():
                torch.mps.empty_cache()
            
            return str(path)
        except Exception as e:
            logging.error(f"이미지 실패: {e}")
            return None