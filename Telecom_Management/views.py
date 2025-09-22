from django.http import JsonResponse
import logging
from rest_framework.decorators import api_view

logger= logging.getLogger('django')


@api_view(['GET'])
def ping(request):
    """
    This is a health check endpoint for the server.
    
    Note: To make this endpoint appear in DRF's Swagger/OpenAPI documentation,
    you should decorate it with @api_view(['GET']) from rest_framework.decorators.
    This tells DRF and drf-spectacular to treat it as an API endpoint.
    """
    logger.info("Ping endpoint was called")
    return JsonResponse({"message": "Server is Running"}, status=200)