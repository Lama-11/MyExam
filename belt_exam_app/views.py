from django.shortcuts import render, redirect
from .models import User, Wish
from django.contrib import messages
import bcrypt


def index(request):
    if 'uid' in request.session:
        return redirect("/wishes")
    context = {
    }
    return render(request, "index.html", context)


def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  
        new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw_hash)
        request.session['uid'] = new_user.id
        return redirect("/wishes")  


def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        logged_user = User.objects.get(email=request.POST['email'])
        request.session['uid'] = logged_user.id
        return redirect('/wishes')
    return redirect("/")


def logout(request):
    request.session.flush()
    return redirect("/")



def wishes_page(request):
    if 'uid' not in request.session:
        return redirect("/")
    context = {
        'user': User.objects.get(id=request.session['uid']),
        'ungranted_wishes': Wish.objects.filter(is_granted=False),
        'granted_wishes': Wish.objects.filter(is_granted=True),
    }

    return render(request, 'dashboard.html', context)


def like_unlike(request, wish_id):
    user = User.objects.get(id=request.session['uid'])
    wish = Wish.objects.get(id=wish_id)
    if user in wish.likes.all():
        wish.likes.remove(user)
    else:
        wish.likes.add(user)
    return redirect('/wishes')


def new_wish_page(request):
    if 'uid' not in request.session:
        return redirect("/")
    context = {
        'user': User.objects.get(id=request.session['uid'])
    }
    return render(request, 'new_wish.html', context)


def create_wish(request):
    if 'uid' not in request.session:
        return redirect("/")
    if request.method == "POST":
        errors =Wish.objects.wish_validator(request.POST) 
        if len(errors) > 0:
            for key, value in errors.items():
                print(errors)
                messages.error(request, value)
            return redirect('/wishes/new')

        new_wish = Wish.objects.create(
            item_name=request.POST['item_name'], 
            description=request.POST['description'], 
            wished_by=User.objects.get(id=request.session['uid'])
        )
    return redirect('/wishes')


def remove(request, wish_id):
    if 'uid' not in request.session:
        return redirect("/")
    wish = Wish.objects.filter(id=wish_id)
    wish.delete()
    return redirect('/wishes')


def edit_page(request, wish_id):
    context = {
        'user': User.objects.get(id=request.session['uid']),
        'wish': Wish.objects.get(id=wish_id),
    }
    return render(request,'edit_wish.html', context)


def edit(request, current_wish_id):
    if request.method == "POST":
        errors =Wish.objects.wish_validator(request.POST) 
        if len(errors) > 0:
            print(errors)
            for key,value in errors.items():
                messages.error(request,value)
            return redirect(f'/wishes/edit/{current_wish_id}')
        wish = Wish.objects.get(id=current_wish_id)
        wish.item_name = request.POST['item_name']
        wish.description = request.POST['description']
        wish.save()
    return redirect('/wishes')


def grant_wish(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
    wish.is_granted = not wish.is_granted
    wish.save()
    return redirect('/wishes')


def stat_page(request):

    context = {
        'user': User.objects.get(id=request.session['uid']),
        'all_granted_wishes': Wish.objects.filter(is_granted=True),
        'user_granted_wishes': User.objects.get(id=request.session['uid']).wishes.filter(is_granted=True),
        'user_ungranted_wishes': User.objects.get(id=request.session['uid']).wishes.filter(is_granted=False),
    }
    return render(request,'stat_page.html', context)


