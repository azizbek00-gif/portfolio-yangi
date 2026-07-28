#!/usr/bin/env bash
# Vercel build: paketlar va static fayllar
pip install -r requirements.txt
python manage.py collectstatic --no-input --clear
