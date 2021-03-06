# coding: utf-8

from django.contrib import admin

from the_tale.blogs.models import Post, Vote


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'votes', 'author', 'state', 'moderator', 'created_at', 'updated_at')

class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'voter', 'post', 'created_at')


admin.site.register(Post, PostAdmin)
admin.site.register(Vote, VoteAdmin)
