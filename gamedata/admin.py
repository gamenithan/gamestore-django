from django.contrib import admin
from django.apps import apps
from gamedata.models import Game_type, Game, User_games, Image
from django.contrib.auth.models import Permission, User

class MyAdd(admin.StackedInline):
    model = Image
    extra = 0

# Register your models here.
class Game_typeadmin(admin.ModelAdmin):
    list_display = ['id', 'type_name']
    list_per_page = 15
#   list_display = ['id', 'question', 'text', 'value']
#     list_per_page = 15
class Gameadmin(admin.ModelAdmin):
    list_display = ['id', 'name','developer', 'price', 'game_type_id']
    list_per_page = 15 

    list_filter = ['release_date', 'price', 'rating', 'developer']
    search_fields = ['name']
    inlines = [ MyAdd ]

    # fieldsets = [
    #     (None, {'fields': ['name', 'rating']}),
    #     ("Active Duration", {'fields': ['release_date'], 'classes': ['collapse']})
    # ]


class User_gameadmin(admin.ModelAdmin):
    list_display = ['id', 'user_id_id', 'game_id_id']
    list_per_page = 15

#   list_display = ['id', 'question', 'text', 'value']
#     list_per_page = 15

try:
    admin.site.register(Permission)
    admin.site.register(Game, Gameadmin)
    admin.site.register(User_games,User_gameadmin)
    admin.site.register(Game_type,Game_typeadmin)
    admin.site.register(Image)
except Exception:
    pass

    
