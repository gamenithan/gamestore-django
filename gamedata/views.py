import datetime
from builtins import object
from datetime import date
from py_compile import main
from urllib import request
import random
import string

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import (login_required,
                                            permission_required,
                                            user_passes_test)
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render

from gamedata.models import Game, Image, User_games


# Create your views here.
def my_login(request):
    logout(request)
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            next_url = request.POST.get('next_url')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')
        else:   
            context['username'] = username
            context['password'] = password
            context['error'] = "Wrong username or password!"
    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url
    return render(request, template_name='login.html', context=context)

@login_required
def my_logout(request):
    logout(request)
    return redirect('login')

@login_required
@permission_required('gamedata.view_user_games')
def user_game(request, num):
    context = {}
    user = request.user.id
    game = Game.objects.get(pk=num)
    gameuser = User_games.objects.all()
    check = 0
    for i in gameuser:
        if i.game_id_id==num and i.user_id_id==user:
            check = 1
    if check==1:
        context['error'] = "Your already have this Game!"
        context['game'] = game
        # return redirect('buygame', num)
        return render(request, 'gamedata/buygame.html', context)
    else:
        post = User_games(
                user_id_id=user,
                game_id_id=num,
                serial='%32x' % random.getrandbits(16*8)
            )
        post.save()

        return redirect('index')
@login_required
@permission_required('gamedata.view_user_games')
def my_lib(request):
    search_txt = request.POST.get('search', '')
    user = request.user.id
    if search_txt == '':
        game = User_games.objects.filter(user_id=user)
        imgs = Image.objects.all()
        return render(request, 'gamedata/gamelib.html', {'games': game, 'imgs':imgs})
        # else:
        #     return render(request, 'gamedata/gamelib.html', {'games': '', 'imgs':''})
    else:
        games = User_games.objects.filter(
        game_id__name__icontains=search_txt, user_id=user
        )
        games2 = User_games.objects.filter(
        game_id__developer__icontains=search_txt, user_id=user
        )
        imgs = Image.objects.filter(game_id__name__icontains=search_txt)
        imgs2 = Image.objects.filter(game_id__developer__icontains=search_txt)
        if games.exists():
            return render(request, 'gamedata/gamelib.html', {'games': games, 'imgs':imgs})
        else:
            return render(request, 'gamedata/gamelib.html', {'games': games2, 'imgs':imgs2})

@login_required
@permission_required('gamedata.view_user_games')
def change_password(request):
    context = {}
    if request.method == 'POST':
        user = request.user
        # user1 = User()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user.set_password(password1)
            user.save()
            # user = authenticate(request, username=user1.username, password=password1)
            # login(request, user)
            return redirect('index')
        else:
            context['password1'] = password1
            context['password2'] = password2
            context['error'] = "password does't match!"

        # check that the passwords match

        # reset password 

    return render(request, template_name='change_password.html', context=context)

def my_regis(request):
    logout(request)
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user_all = User.objects.all()
        check = 0
        if username != '' and password != '':
            for i in user_all:
                if i.username == username:
                    check = 1
                elif password2 != password:
                    check = 2
            if check == 0:
                user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
                user.set_password(password)
                group = Group.objects.get(name='user')
                user.groups.add(group)
                user.save()
                return redirect('index')
            elif check == 1:
                context['error'] = "already have this userename!"
                return render(request, 'gamedata/regis.html', context=context)
            else:
                context['error'] = "รหัสไม่ตรงกัน"
                return render(request, 'gamedata/regis.html', context=context)
        else:
            context['error'] = "กรุณากรอกข้อมูล"
            return render(request, 'gamedata/regis.html', context=context)

    else:
        return render(request, 'gamedata/index.html')

def index(request):
    
    return render(request, 'gamedata/index.html')

def home_page(request):
    games = Game.objects.all()   
    imgs = Image.objects.all()
    games2 = Game.objects.filter(game_type_id=3)
    imgs2 = Image.objects.filter(game_id__game_type_id=3)
    games3 = Game.objects.filter(game_type_id=4)
    imgs3 = Image.objects.filter(game_id__game_type_id=4)
    games4 = Game.objects.filter(game_type_id=1)
    imgs4 = Image.objects.filter(game_id__game_type_id=1)
    games5 = Game.objects.filter(game_type_id=2)
    imgs5 = Image.objects.filter(game_id__game_type_id=2)
    # raw = []
    # raw.append(imgs)
    result = zip(games[:5], imgs[:5])
    result2 = zip(games2[:5], imgs2[:5])
    result3 = zip(games3[:5], imgs3[:5])
    result4 = zip(games4[:5], imgs4[:5])
    result5 = zip(games5[:5], imgs5[:5])
    return render(request, 'gamedata/index.html', context={
        'result' : result,
        'result2' : result2,
        'result3' : result3,
        'result4' : result4,
        'result5' : result5
    })

def my_all(request):
    search_txt = request.POST.get('search', '')
    if search_txt == '':        
        games = Game.objects.all()   
        imgs = Image.objects.all()
        # raw = []
        # raw.append(imgs)
        result = zip(games, imgs)
        return render(request, 'gamedata/all.html', context={
            'result' : result
        })
    else:
        games = Game.objects.filter(
        name__icontains=search_txt
        )
        games2 = Game.objects.filter(
        developer__icontains=search_txt
        )
        imgs = Image.objects.filter(game_id__name__icontains=search_txt)
        imgs2 = Image.objects.filter(game_id__developer__icontains=search_txt)
        if games.exists():
            result = zip(games, imgs)
        else:
            result = zip(games2, imgs2)
        return render(request, 'gamedata/all.html', context={
            'result' : result,
            'search_txt' : search_txt
        })

def my_filter(request):
    temp = request.POST.get('game_type')
    games = Game.objects.all()  
    imgs = Image.objects.all()

    # raw = []
    # raw.append(imgs)
    result = zip(games, imgs)
    
    print(temp)
    return render(request, 'gamedata/filter.html', context={
        'result' : result,
        'temp' : temp
    })

def game_list(request, game_num):
    game = Game.objects.get(pk=game_num)
    img = Image.objects.get(pk=game_num)
    return render(request, 'gamedata/list.html', { 'game': game, 'img': img})
    #  context={
    #     'name': game[0].name
    # }
@login_required
@permission_required('gamedata.view_user_games')
def my_buygame(request, buy_num):
    game = Game.objects.get(pk=buy_num)
    return render(request, 'gamedata/buygame.html', {'game': game})
def regis(request):
    logout(request)
    return render(request, 'gamedata/regis.html')
@login_required
def my_edit(request):
    user = request.user
    return render(request, 'gamedata/edit.html', context={
        'user':user
    })
@login_required
def after_edit(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        temp = User.objects.filter(id=user.id).update(username=username, first_name=first_name, last_name=last_name, email=email)
        return redirect('edit')


def show_error_404(request):
    foo = False
    if foo:
        return HttpResponseNotFound('404')
    else:
        return redirect(to='list')
