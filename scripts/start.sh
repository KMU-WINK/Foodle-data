#!/usr/bin/env bash

PROJECT_ROOT="/home/ubuntu/app"
TARGET_DIR="$PROJECT_ROOT/Foodle-data/foodle"

APP_LOG="$PROJECT_ROOT/application.log"
ERROR_LOG="$PROJECT_ROOT/error.log"
DEPLOY_LOG="$PROJECT_ROOT/deploy.log"

TIME_NOW=$(date +%c)

# dependency 설치
pip install -r requirements.txt

# 서버 실행
echo "$TIME_NOW > 파일 실행" >> $DEPLOY_LOG
nohup python $TARGET_DIR/manage.py runserver 0.0.0.0:8000 &

CURRRENT_PID = $(pgrep -f "python3 manage.py runserver")
echo "$TIME_NOW > 실행된 프로세스 아이디 $CURRENT_PID 입니다." >> $DEPLOY_LOG