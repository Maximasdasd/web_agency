from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import requests
import json
from django.conf import settings
from django.http import HttpResponse



def home(request):
    return render(request, "index3.html")

def test(request):
    return render(request, "index.html")

def lead_submit(request):
    """
    Обработка отправки формы заявки (лид-форма)
    """
    print('start')
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        telegram = request.POST.get('telegram', '').strip()
        category_map = {
        'Лендинг': 'landing',
        'Сайт компании': 'site',
        'Интернет-магазин': 'internetshop',
        'Telegram-бот': 'tgbot',
        'Доработка сайта': 'rework',
        'Пока не определился': 'undecided'
        }
        category_ru = request.POST.get('category', 'Пока не определился').strip()
        category = category_map.get(category_ru, 'undecided')
        description = request.POST.get('description', '').strip()
        print(name)
        # Валидация обязательных полей
        if not name or not phone:
            messages.error(request, 'Пожалуйста, заполните имя и телефон')
            return redirect('home')
        
        # Подготовка данных для отправки в FastAPI
#   "name": "string",
#   "email": "string",
#   "phone": "string",
#   "telegram": "string",
#   "category": "landing"
        lead_data = {
            "name": name,
            "email": email or None,
            "phone": phone,
            "telegram": telegram.replace('@', '') if telegram else None,
            "category": category,
            "description": description,
        }
        
        # Отправляем в FastAPI (сохраняем в БД через API)
        try:
            response = requests.post(
                f"{settings.FASTAPI_URL}/ticket/create_ticket",  # твой эндпоинт
                json=lead_data,
                timeout=10
            )
            
            if response.status_code == 201:
                messages.success(request, 'Заявка успешно отправлена! с вами свяжутся в ближайшее время.')
                
                # Отправляем уведомление в Telegram
                try:
                    send_telegram_message(lead_data)
                except:
                    pass
            else:
                error_msg = response.json().get('detail', 'Неизвестная ошибка')
                messages.error(request, f'Ошибка: {error_msg}')
                
        except requests.exceptions.ConnectionError:
            messages.error(request, 'Не удалось подключиться к серверу')
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')
        
        return redirect('home')
    
    return redirect('home')


def send_telegram_message(lead_data):
    """Отправка сообщения в Telegram"""
    
    text = f"🆕 **НОВАЯ ЗАЯВКА**\n\n"
    text += f"👤 **Имя:** {lead_data['name']}\n"
    text += f"📞 **Телефон:** {lead_data['phone']}\n"
    
    if lead_data.get('email'):
        text += f"📧 **Почта:** {lead_data['email']}\n"
    if lead_data.get('telegram'):
        text += f"💬 **Telegram:** @{lead_data['telegram']}\n"
    
    text += f"📂 **Категория:** {lead_data['category']}\n"
    
    if lead_data.get('description'):
        text += f"\n📝 **Описание:**\n{lead_data['description']}\n"
    
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload, proxies=settings.TELEGRAM_PROXY, timeout=10)