from django.http import JsonResponse
import logging

logger= logging.getLogger('django')

def ping(request):
    logger.info("Ping endpoint was called")
    return JsonResponse({"message": "Server is Running"}, status=200)