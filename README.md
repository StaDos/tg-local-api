# Telegram → Local JSON API (Termux)

Полностью локальный Telegram-бот с FastAPI, сохраняет все сообщения в `data.json`  
Работает на Android без внешних серверов, веб-серверов и облаков.

## Особенности
- Бот отвечает на любые сообщения  
- Все данные сохраняются в `data.json`  
- Доступ через браузер: `http://твой_IP:8000/data`  
- Swagger UI: `http://твой_IP:8000/docs`  
- Запускается в Termux одной командой

## Запуск
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
