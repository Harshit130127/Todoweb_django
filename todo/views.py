from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from todo import models
from todo.models import TodoItem
from django.contrib.auth.decorators import login_required

# User Signup View 
def signup(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email_id = request.POST.get("email_id")
        password = request.POST.get("password")
        print(f"Full Name: {full_name}, Email ID: {email_id}, Password: {password}")
        
        try:
            # Create new user account
            my_user = User.objects.create_user(full_name, email_id, password)
            my_user.save()
            return redirect("/login")
        except Exception as e:
            print("Error during signup:", e)
            return render(request, "signup.html", {"error": "Signup failed. Try again."})

    return render(request, "signup.html")

# User Login View 
def login_user(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        passwords = request.POST.get("password")

        # Authenticate credentials
        userr = authenticate(request, username=full_name, password=passwords)
        if userr is not None:
            login(request, userr)
            return redirect("/todo")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")

# Todo List 
@login_required(login_url='/login')
def todo_list(request):
    if request.method == "POST":
        title = request.POST.get("title")
        print(f"Title: {title}")

        try:
            # Save new todo item
            todo = models.TodoItem(title=title, user=request.user)
            todo.save()
        except Exception as e:
            print("Error saving todo:", e)
            return render(request, "todo.html", {
                "user_todo_list": models.TodoItem.objects.filter(user=request.user).order_by("-date"),
                "error": "Failed to add item."
            })

    # Show list regardless of POST/GET
    user_todo_list = models.TodoItem.objects.filter(user=request.user).order_by("-date")
    return render(request, "todo.html", {"user_todo_list": user_todo_list})

#  Edit Todo 
@login_required(login_url='/login')
def edit_todo(request, serial_number):
    try:
        obj = models.TodoItem.objects.get(serial_number=serial_number, user=request.user)
    except TodoItem.DoesNotExist:
        return redirect("/todo")

    if request.method == "POST":
        title = request.POST.get("title")
        obj.title = title
        obj.save()
        return redirect('/todo')

    return render(request, 'edit_todo.html', {'obj': obj})

# Delete Todo 
@login_required(login_url='/login')
def delete_todo(request, serial_number):
    try:
        obj = models.TodoItem.objects.get(serial_number=serial_number, user=request.user)
        obj.delete()
    except TodoItem.DoesNotExist:
        pass  
    return redirect('/todo')

# Logout User 
@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return redirect('/login')

# Mark Todo as Completed 
@login_required(login_url='/login')
def mark_done(request, serial_number):
    if request.method == "POST":
        try:
            todo = get_object_or_404(TodoItem, serial_number=serial_number, user=request.user)
            todo.status = True
            todo.save()
        except Exception as e:
            print("Failed to mark as done:", e)
    return redirect("/todo")
