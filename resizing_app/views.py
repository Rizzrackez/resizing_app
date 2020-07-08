from django.http import JsonResponse


def custom404(request, exception=None):
    """Обработчик несуществующих страниц"""
    return JsonResponse(status=404, data={
        'status_code': 404,
        'error': 'The resource was not found'
    })
