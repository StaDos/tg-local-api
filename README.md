# Telegram → Local API (Termux)

Бот принимает любые сообщения и сохраняет их в data.json  
Запускается в Termux на телефоне

## Запуск

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
