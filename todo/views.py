from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required




def home(request):
    return render(request, 'todo/home.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})

    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/signupuser.html', {'form':AuthenticationForm(), 'error':'Username and password doses not match'})

        else:
                login(request, user)
                return redirect('currenttodos')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')

            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Username already exist. Please choose a different username'})
        else:
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Password did not match'})

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def currenttodos(request):
    #to displa all the objects in todos
    #filter is used to filter out a the todos of requested user
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', { 'todos':todos })

@login_required
def completedtodos(request):
        todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
        return render(request, 'todo/completedtodos.html', { 'todos':todos })

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})

    else:
        try:
            #to post some information to the todo, after clicking create button
            #to check whether the request is a POST
            form = TodoForm(request.POST)
            #to save the todo but dont commit it in databases
            newtodo = form.save(commit=False)
            #save the todo for a particular username
            newtodo.user = request.user
            #to commit it to databases
            newtodo.save()
            #redirect tocurrent todo page
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in, try again'})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk, user=request.user)
    if request.method == 'GET':
            form = TodoForm(instance=todo)
            return render(request, 'todo/viewtodo.html', { 'todo':todo, 'form':form })
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', { 'todo':todo, 'form':form, 'error':'Bad info' })

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
