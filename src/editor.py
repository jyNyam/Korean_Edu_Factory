import os
import logging
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from config import *

# =========================================================
# [핵심 수정] MoviePy 버전 호환성 해결
# 최신 버전(2.0 이상)과 구버전(1.0) 모두 작동하도록 설정
# =========================================================
try:
    from moviepy import * # 최신 버전 (v2.0+)
except ImportError:
    from moviepy.editor import * # 구버전 (v1.0)

logging.basicConfig(filename=LOGS_DIR / 'editor.log', level=logging.INFO)

class EditorEngine:
    @staticmethod
    def add_caption(img_path, text):
        """
        이미지 하단에 자막 바와 텍스트를 합성하는 함수
        """
        try:
            img = Image.open(img_path).convert("RGBA")
            W, H = img.size
            draw = ImageDraw.Draw(img)
            
            # 폰트 설정
            try:
                font = ImageFont.truetype(FONT_PATH, int(H*0.08))
            except:
                font = ImageFont.load_default()
            
            # 글자 크기 및 위치 계산
            bbox = draw.textbbox((0,0), text, font=font)
            w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
            x, y = (W-w)/2, H-(h*1.8)
            
            # 자막 배경(반투명 흰색) 및 글자 쓰기
            draw.rectangle([x-10, y-10, x+w+10, y+h+10], fill=(255,255,255,200))
            draw.text((x,y), text, font=font, fill="black")
            
            return np.array(img.convert("RGB"))
        except Exception as e:
            logging.error(f"자막 실패: {e}")
            return str(img_path)

    @staticmethod
    def create_video(img_path, aud_path, out_path, text):
        """
        이미지와 오디오를 합쳐 영상을 만드는 함수
        """
        try:
            # 1. 오디오 불러오기
            audio = AudioFileClip(str(aud_path))
            
            # 2. 자막 입힌 이미지 불러오기
            captioned_img = EditorEngine.add_caption(img_path, text)
            
            # 3. 이미지 영상을 오디오 길이만큼 늘리기 (+0.5초 여유)
            # (최신 버전 호환을 위해 복잡한 효과는 제외하고 기본 합치기만 수행)
            clip = ImageClip(captioned_img).set_duration(audio.duration + 0.5)
            clip = clip.set_audio(audio).set_position('center')
            
            # 4. 영상 저장 (Mac 가속 코덱 사용)
            clip.write_videofile(
                str(out_path), 
                fps=VIDEO_FPS, 
                codec='h264_videotoolbox', 
                audio_codec='aac', 
                threads=4, 
                logger=None
            )
            return str(out_path)
        except Exception as e:
            logging.error(f"편집 실패: {e}")
            return None