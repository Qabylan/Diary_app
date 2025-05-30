from django.urls import path
from .views import home, register_view, login_view, logout_view, add_entry, memories_view, add_memory

urlpatterns = [
    path('home/', home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add/', add_entry, name='add'),
    path('memories/', memories_view, name='memories'),
    path('memories/add/', add_memory, name='add_memory')
]