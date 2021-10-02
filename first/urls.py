from django.urls import path, include
from .views import Register, LoginView, UserDetails

urlpatterns = [
    path('register', Register.as_view()),
    path('login', LoginView.as_view()),
    path('<int:id>', UserDetails.as_view()),
]
