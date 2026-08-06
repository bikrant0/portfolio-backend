from django.contrib import admin
from .models import PortfolioProject, TechStack

@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)
    list_filter = ('category',)

@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    # Colums in the table view
    list_display = ('title', 'is_published','created_at')

    # Sidebar filter
    list_filter = ('is_published','tech_stacks')

    # Search Bar
    search_fields = ('title', 'description')

    # Automatically fills out slug field
    prepopulated_fields = {'slug':('title',)}

    # Makes it easier to select Many-To-Many relationships
    filter_horizontal = ('tech_stacks',)



    

