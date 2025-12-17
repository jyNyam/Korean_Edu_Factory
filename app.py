# app.py
import streamlit as st
import sys
from pathlib import Path
import os

# [중요] 멀티프로세싱 경고 차단
os.environ["TOKENIZERS_PARALLELISM"] = "false"

sys.path.append(str(Path(__file__).parent / 'src'))

from brain import BrainEngine
from visual import VisualEngine
from audio import AudioEngine
from editor import EditorEngine
from config import *

st.set_page_config(page_title="M1 영상 공장", layout="wide")
st.title("🏭 M1 한국어 교육 영상 공장 (MLX Edition)")

# 엔진 초기화
if 'visual' not in st.session_state:
    st.session_state.visual = VisualEngine()
    st.session_state.audio = AudioEngine()
    st.session_state.brain = BrainEngine()

with st.sidebar:
    st.header("설정")
    topic = st.text_input("주제 입력", "병원")
    count = st.slider("단어 개수", 1, 5, 3)

if st.button("🎬 영상 생성 시작", type="primary"):
    with st.status("🚀 작업 진행 중...", expanded=True) as status:
        
        st.write("🧠 AI가 기획 중입니다...")
        data = st.session_state.brain.generate_vocabulary_data(topic, count)
        
        if data:
            st.write(f"✅ 기획 완료: {len(data['words'])}개 단어")
            
            for i, item in enumerate(data['words']):
                idx = i + 1; word = item['korean']
                p_img = IMAGES_DIR / f"{topic}_{idx}.png"
                p_aud = AUDIO_DIR / f"{topic}_{idx}.mp3"
                p_vid = FINAL_DIR / f"{topic}_{idx}_{word}.mp4"
                
                st.write(f"---")
                st.write(f"🎨 [{idx}/{count}] '{word}' 제작 중...")
                
                # 이미지 -> 오디오 -> 영상 순서로 생성
                st.session_state.visual.generate_image(item['image_prompt'], p_img)
                st.image(str(p_img), width=300)
                
                st.session_state.audio.generate_audio(f"{word}. {item['example']}", p_aud)
                EditorEngine.create_video(p_img, p_aud, p_vid, word)
                
                col, _ = st.columns(2)
                with col:
                    if p_vid.exists():
                        st.video(str(p_vid))
            
            status.update(label="🎉 모든 작업 완료!", state="complete")