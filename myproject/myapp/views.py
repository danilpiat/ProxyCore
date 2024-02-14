from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Operation
from .parse_configs import parseConfigPath

@csrf_exempt
def index(request):
    if request.method == 'POST':
        # Пометим, что операция выполняется
        operation = Operation.objects.create(status='Выполняется')
        try:
            parseConfigPath()
            operation.status = 'Успешно'
            operation.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            # Если есть ошибка, то
            operation.status = 'Ошибка: ' + str(e)
            operation.save()
            return JsonResponse({'status': 'error', 'message': str(e)})
    return render(request, 'myapp/index.html')


