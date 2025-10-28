from django.contrib import admin
from .models import Category, Ad, Comment, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.
    Displays:
        - name: The name of the category.
        - description: A brief description of the category.
        - active_ads_count: A custom method showing the number of active ads
        in this category.
    """
    list_display: tuple[str, ...] = ('name', 'description', 'active_ads_count')


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Ad model.
    Displays:
        - title: The title of the ad.
        - price: The listed price.
        - is_active: Whether the ad is currently active.
        - category: The category the ad belongs to.
        - user: The user who posted the ad.
        - created_at: The date the ad was created.
    Filters:
        - is_active: Filter ads by active/inactive status.
        - category: Filter ads by category.
    """
    list_display: tuple[str, ...] = (
        'title', 'price', 'is_active', 'category', 'user', 'created_at'
    )
    list_filter: tuple[str, ...] = ('is_active', 'category')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Comment model.
    Displays:
        - ad: The ad this comment belongs to.
        - user: The user who posted the comment.
        - created_at: The date the comment was created.
    """
    list_display: tuple[str, ...] = ('ad', 'user', 'created_at')


admin.site.register(UserProfile)
