from rest_framework import serializers
from .models import PortfolioProject, TechStack

class TechStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechStack
        fields = ['id', 'name','category']

class PortfolioProjectSerializer(serializers.ModelSerializer):
    tech_stacks = TechStackSerializer(many=True, read_only=True)

    class Meta:
        model = PortfolioProject
        fields = [
            'id', 
            'title', 
            'slug', 
            'description', 
            'github_url', 
            'swagger_url', 
            'architecture_url', 
            'tech_stacks', 
            'created_at'            
        ]

class EchoPayloadSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=500, required=True)