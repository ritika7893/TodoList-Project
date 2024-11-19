from django import forms
from .models import Todo
from django.contrib.auth import authenticate


from django.contrib.auth.models import (
    User,
)  # Assuming you're using the built-in User model


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"}),
        required=True,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm your password"}),
        required=True,
    )

    class Meta:
        model = User  # Change to `User` if you are not using `Customer`
        fields = ["username", "email", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Create a username"}),
            "email": forms.EmailInput(attrs={"placeholder": "Enter your email"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        username = cleaned_data.get("username")

        # Validate that the passwords match
        if password != confirm_password:
            self.add_error("confirm_password", "The two password fields must match.")

        # Validate that the username is unique
        if username and User.objects.filter(username=username).exists():
            self.add_error(
                "username", "Username already exists. Please choose another."
            )

        return cleaned_data

    def save(self, commit=True):
        # Save the user with the hashed password
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            user.save()
        return user


class CustomLoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}), required=True
    )


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["todo_name"]  # Make sure this matches your model
        widgets = {
            "todo_name": forms.TextInput(attrs={"placeholder": "Enter a task here"}),
        }
