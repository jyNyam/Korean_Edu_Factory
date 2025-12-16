from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import logging
from config import *

logging.basicConfig(filename=LOGS_DIR / 'editor.log', level=logging.INFO)

class EditorEngine:
    @staticmethod
    def add_caption(img_path, text):
        """
        이미지 하단에 반투명한 흰색 박스를 만들고 그 위에 자막을 쓰는 함수
        """
        try:
            # 1. 이미지를 엽니다.
            img = Image.open(img_path).convert("RGBA")
            W, H = img.size
            draw = ImageDraw.Draw(img)
            
            # 2. 폰트 설정 (Mac 기본 폰트 사용)
            try:
                font = ImageFont.truetype(FONT_PATH, int(H*0.08)) # 글자 크기: 높이의 8%
            except:
                font = ImageFont.load_default() # 폰트가 없으면 기본 폰트(한글 깨질 수 있음)
            
            # 3. 글자 크기 계산 (중앙 정렬을 위해)
            bbox = draw.textbbox((0,0), text, font=font)
            w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
            x, y = (W-w)/2, H-(h*1.8) # 위치 계산
            
            # 4. 자막 배경 박스 그리기 (흰색, 투명도 200)
            draw.rectangle([x-10, y-10, x+w+10, y+h+10], fill=(255,255,255,200))
            
            # 5. 글자 쓰기 (검은색)
            draw.text((x,y), text, font=font, fill="black")
            
            # 6. MoviePy가 이해할 수 있는 형태(Numpy 배열)로 변환
            return np.array(img.convert("RGB"))
        except Exception as e:
            logging.error(f"자막 실패: {e}")
            return str(img_path) # 실패하면 그냥 원본 이미지 리턴

    @staticmethod
    def create_video(img_path, aud_path, out_path, text):
        try:
            # 1. 오디오 파일 로드
            audio = AudioFileClip(str(aud_path))
            
            # 2. 이미지에 자막 입히고, 영상 클립으로 변환 (길이는 오디오 + 0.5초)
            captioned_img = EditorEngine.add_caption(img_path, text)
            clip = ImageClip(captioned_img).set_duration(audio.duration + 0.5)
            
            # 3. 줌인 효과(resize) 및 오디오 합체
            clip = clip.set_audio(audio).resize(lambda t: 1 + 0.04*t).set_position('center')
            
            # 4. 최종 영상 저장 (Mac 하드웨어 가속 코덱 사용)
            clip.write_videofile(
                str(out_path), 
                fps=VIDEO_FPS, 
                codec='h264_videotoolbox', # Mac M1 전용 초고속 코덱
                audio_codec='aac', 
                threads=4, 
                logger=None
            )
            return str(out_path)
        except Exception as e:
            logging.error(f"편집 실패: {e}")
            return None