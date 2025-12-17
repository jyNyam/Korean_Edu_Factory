#!/bin/bash

# 1. 프로젝트 폴더로 이동 (경로 자동 인식)
cd "$(dirname "$0")"

# 2. 메모리 청소 (비밀번호 1회 입력 필요)
echo "🧹 Mac 메모리를 정리합니다 (Password를 입력하세요)..."
sudo purge

# 3. 가상환경 활성화 및 실행
source .venv/bin/activate
echo "🚀 영상 공장을 가동합니다..."
streamlit run app.py --server.maxUploadSize=500
