from django.urls import path
from . import views

urlpatterns = [
            path('home/', views.home_view, name='home'),
            path('about/', views.about_view, name='about'),
            path('events/', views.events_view, name='events'),
            path('members/', views.members_view, name='members'),
            path('gallery/', views.gallery_view, name='gallery'),
            path('join/', views.join_view, name='join'),
            path('contact/', views.contact_view, name='contact'),
            path('president-message/', views.president_message_view, name='president-message'),
]
