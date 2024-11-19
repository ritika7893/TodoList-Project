from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.contrib import messages

from django.contrib.auth.hashers import check_password  # For password validation

# Your custom user model
from .forms import CustomLoginForm, RegisterForm

from django.contrib.auth.views import LogoutView
from .models import Todo
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Todo
from django.contrib.auth.decorators import login_required
from .forms import TodoForm


@login_required
def DeleteTask(request, name):
    get_todo = get_object_or_404(
        Todo, user=request.user, todo_name=name
    )  # Use get_object_or_404 for better error handling
    get_todo.delete()
    return redirect("home-page")


@login_required
def Update(request, name):
    get_todo = get_object_or_404(
        Todo, user=request.user, todo_name=name
    )  # Use get_object_or_404 for better error handling
    get_todo.status = True  # Mark the task as completed
    get_todo.save()
    return redirect("home-page")


class Login(FormView):
    template_name = "todoapp/login.html"
    success_url = reverse_lazy("home-page")  # Redirect after successful login
    form_class = CustomLoginForm

    def dispatch(self, request, *args, **kwargs):
        # Redirect to home page if user is already authenticated
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Get cleaned data from the form
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)  # Log the user in
            return super().form_valid(form)  # Proceed to the success URL
        else:
            # If authentication fails, add an error message and return invalid form
            messages.error(
                self.request, "Error, wrong user details or user does not exist"
            )
            return self.form_invalid(form)


class Index(LoginRequiredMixin, FormView):
    template_name = "todoapp/todo.html"

    def get(self, request, *args, **kwargs):
        all_todos = Todo.objects.filter(user=request.user)
        context = {
            "todos": all_todos,
            "form": TodoForm(),  # Initialize a new form instance
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        task = request.POST.get("todo_name")  # Correctly get the task name
        if task:
            new_todo = Todo(user=request.user, todo_name=task)
            new_todo.save()
        return redirect("home-page")  # Redirect to the home page after saving


class Register(FormView):
    template_name = "todoapp/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("login-page")  # Redirect after successful registration

    def form_valid(self, form):
        # Save the form and create the new user
        form.save()

        # Add a success message
        messages.success(self.request, "User successfully created. You can now log in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Add an error message if the form is invalid
        messages.error(
            self.request,
            "There were errors in your form. Please fix them and try again.",
        )
        return super().form_invalid(form)


class Logout(LogoutView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login-page")
