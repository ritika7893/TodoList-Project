from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="home-page"),
    path(
        "delete/<str:name>/", views.DeleteTask, name="delete"
    ),  # URL for deleting a task
    path("update/<str:name>/", views.Update, name="update"),
    path("register/", views.Register.as_view(), name="register"),
    path("login/", views.Login.as_view(), name="login-page"),
    path("logout/", views.Logout.as_view(next_page="login-page"), name="logout"),
]
