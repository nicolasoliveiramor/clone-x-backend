from django.contrib import admin
from .models import Post, Like, Comment, Retweet

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_at')
    search_fields = ('content', 'author__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    autocomplete_fields = ('user', 'post')
    list_select_related = ('user', 'post')
    date_hierarchy = 'created_at'

@admin.register(Retweet)
class RetweetAdmin(admin.ModelAdmin):
    autocomplete_fields = ('user', 'post')
    list_select_related = ('user', 'post')
    date_hierarchy = 'created_at'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'short_content', 'created_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)
    autocomplete_fields = ('author', 'post')
    list_select_related = ('author', 'post')
    date_hierarchy = 'created_at'

    @admin.display(description='content', ordering='content')
    def short_content(self, obj):
        return (obj.content[:80] + '...') if len(obj.content) > 80 else obj.content

