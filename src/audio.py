import edge_tts
import asyncio
import logging
from config import *

logging.basicConfig(filename=LOGS_DIR / 'audio.log', level=logging.INFO)

class AudioEngine:
    def generate_audio(self, text, path):
        # 비동기 함수 실행을 위한 껍데기 함수
        asyncio.run(self._gen(text, path))

    async def _gen(self, text, path):
        try:
            # TTS 생성 및 저장
            communicate = edge_tts.Communicate(text, TTS_VOICE, rate="-5%")
            await communicate.save(str(path))
        except Exception as e:
            logging.error(f"녹음 실패: {e}")