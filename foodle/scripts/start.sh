#!/usr/bin/env bash

PROJECT_ROOT="/home/ubuntu/app"
TARGET_DIR="$PROJECT_ROOT/Foodle-data/foodle"

# 서버 실행
nohup python $TARGET_DIR/manage.py runserver 0.0.0.0:8000 &