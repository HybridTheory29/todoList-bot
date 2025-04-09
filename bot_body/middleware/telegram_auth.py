from django.http import JsonResponse
from django.conf import settings

class TelegramWebhookAuth:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверяем только запросы к вебхуку
        if request.path == '/api/telegram-webhook/':
            secret = request.headers.get('X-Telegram-Secret')
            
            # Сравниваем с секретным ключом из settings.py
            if secret != settings.TELEGRAM_WEBHOOK_SECRET:
                return JsonResponse({'error': 'Invalid secret'}, status=403)
                
        return self.get_response(request)