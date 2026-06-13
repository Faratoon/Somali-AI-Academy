"""
Somali AI Academy — Telebot1 v3
Bot-ka rarista: python3 main.py
"""
import sys
import os

# Ensure telebot1 package is importable
sys.path.insert(0, os.path.dirname(__file__))

from telebot1.main import main

if __name__ == "__main__":
    main()
