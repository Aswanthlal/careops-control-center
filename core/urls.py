"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from workspace.views import dashboard, inbox, dashboard_data, get_conversations, get_messages, send_reply,bookings_page
from workspace.views import get_bookings, update_booking_status
from workspace.views import seed_demo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard),
    path('inbox/', inbox),
    path('bookings/',bookings_page),

    path('api/dashboard/', dashboard_data),
    path('api/conversations/', get_conversations),
    path('api/messages/<int:conv_id>/', get_messages),
    path('api/send-reply/', send_reply),
    path('api/bookings/', get_bookings),
    path('api/update-booking/', update_booking_status),
    path('seed-demo/', seed_demo),
    
]

