from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

@api_view(['GET'])
def health_check(request):
    payload = {
        "status":"healthy",
        "version":"1.0.0",
        "message":"Portfolio API is running smoothly.",
        "timestamp":datetime.now().isoformat(),
    }
    return Response(payload, status=status.HTTP_200_OK)
    