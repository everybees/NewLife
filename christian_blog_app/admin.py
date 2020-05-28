from django.contrib import admin
from .models import Post, Article, Prayer, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'slug', 'status', 'created_date', 'published_date' )
    list_display_links = ('id', 'title')
    list_filter = ('title', 'published_date', 'author')
    list_editable = ('published_date',)
    search_fields = ('title', 'author', 'title', 'created_date', 'published_date')
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 25

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'article', 'article_date')
    list_filter = ('author', 'title', 'article_date')
    search_fields = ('author','title')
    list_per_page = 25

class PrayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'prayer_date')
    list_filter = ('username', 'prayer_date')
    list_per_page = 25


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Prayer, PrayerAdmin)
admin.site.register(Comment, CommentAdmin)