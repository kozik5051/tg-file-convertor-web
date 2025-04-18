#!/bin/bash

# Установка FFmpeg
curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz -o ffmpeg.tar.xz
tar -xf ffmpeg.tar.xz
mv ffmpeg-*-amd64-static/ffmpeg /usr/local/bin/
chmod +x /usr/local/bin/ffmpeg

# Установка LibreOffice (если используешь word_to_pdf)
apt-get update && apt-get install -y libreoffice
