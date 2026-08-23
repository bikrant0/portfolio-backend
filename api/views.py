import hashlib
import time
from django.shortcuts import render
from rest_framework.decorators import APIView, api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle
from datetime import datetime
from .serializers import PortfolioProjectSerializer, EchoPayloadSerializer
from .models import PortfolioProject, ApiPlaygroundLog
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend



@api_view(['GET'])
def health_check(request):
    payload = {
        "status":"healthy",
        "version":"1.0.0",
        "message":"Portfolio API is running smoothly.",
        "timestamp":datetime.now().isoformat(),
    }
    return Response(payload, status=status.HTTP_200_OK)


class ProjectListAPIView(generics.ListAPIView):

    serializer_class = PortfolioProjectSerializer
    throttle_scope = 'portfolio_views'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    search_fields = ['title','description', 'tech_stacks__name']

    filterset_fields = ['is_published']

    def get_queryset(self):
        return PortfolioProject.objects.filter(is_published=True).prefetch_related('tech_stacks')  

class ProjectDetailAPIView(generics.RetrieveAPIView):

    serializer_class = PortfolioProjectSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return PortfolioProject.objects.filter(is_published=True).prefetch_related('tech_stacks')      

class EchoPlaygroundAPIView(APIView):
    # Receives a Json payload, calculate latency and logs it and echoes it back.
    throttle_scope = 'playground_echo'

    def post(self, request, *args, **kwargs):
        # 1. Starts stopwatch
        start_time = time.time()

        # 2. Validates incoming JSON
        serializer = EchoPayloadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 3. Grabs IP from request headers
        raw_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        ip_hash = hashlib.sha256(raw_ip.encode('utf-8')).hexdigest()
        
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')

        # 4. Stop stopwatch and calculate milliseconds
        end_time = time.time()
        latency_ms = int((end_time - start_time) * 1000)

        # 5. Log it to database
        ApiPlaygroundLog.objects.create(
            latency_ms=latency_ms,
            ip_hash=ip_hash,
            user_agent=user_agent
        )

        # 6. Prepare   dynamic response
        response_data = {
            "received_message": serializer.validated_data['message'],
            "server_latency_ms": latency_ms,
            "status": "Echo successful"
        }

        return Response(response_data, status=status.HTTP_200_OK)

                            