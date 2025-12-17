import torch
from diffusers import FluxPipeline
import logging
import gc
from config import *

logging.basicConfig(filename=LOGS_DIR / 'visual.log', level=logging.INFO)

class VisualEngine:
    def __init__(self):
        self.pipe = None # 처음엔 붓을 들고 있지 않음 (메모리 절약)

    def load_model(self):
        # 그림 그릴 때만 모델을 불러옵니다.
        if not self.pipe:
            self.pipe = FluxPipeline.from_pretrained(
                FLUX_MODEL, 
                torch_dtype=torch.bfloat16, 
                cache_dir=MODELS_DIR
            )
            self.pipe.enable_model_cpu_offload()

    def generate_image(self, prompt, path):
        self.load_model()
        try:
            # 그림 생성 명령
            img = self.pipe(prompt, height=IMAGE_SIZE, width=IMAGE_SIZE, num_inference_steps=4, guidance_scale=0.0).images[0]
            img.save(path) # 저장
            return str(path)
        except Exception as e:
            logging.error(f"이미지 실패: {e}")
            return None
            
    def unload_model(self):
        # 작업이 끝나면 메모리를 비워줍니다.
        if self.pipe:
            del self.pipe
            self.pipe = None
            gc.collect()
            torch.mps.empty_cache()