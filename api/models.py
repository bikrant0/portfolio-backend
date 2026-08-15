from django.db import models
import uuid

class TechStack(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50, help_text="E.g: Frontend, Backend, Database")

    def __str__(self):
        return self.name

class PortfolioProject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=120, unique=True, help_text="Used for clean URLs")
    description = models.TextField()

    # URLs for recruiter to verify my work
    github_url = models.URLField(blank=True, null=True)
    swagger_url = models.URLField(blank=True, null=True)
    architecture_url = models.URLField(blank=True, null=True)

    #Status and timestamps
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Relationships
    tech_stacks = models.ManyToManyField(TechStack, related_name="projects")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_at']

class ApiPlaygroundLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    endpoint = models.CharField(max_length=100, default="/api/v1/playground/echo/")
    method = models.CharField(max_length=10, default="POST")
    latency_ms = models.IntegerField(help_text="Response time in milliseconds")
    response_status = models.IntegerField(default=200)
    
    # hasing IP for privacy
    ip_hash = models.CharField(max_length=256)
    user_agent = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Echo Request - {self.latency_ms}ms at {self.timestamp}"
        
    class Meta:
        ordering = ['-timestamp']
