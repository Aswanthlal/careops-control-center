from django.shortcuts import render
from django.db import models

# Create your views here.

def dashboard(request):
    return render(request, "workspace/dashboard.html")

def bookings_page(request):
    return render(request, "workspace/bookings.html")


from django.http import JsonResponse
from django.utils import timezone
from datetime import date
from .models import Booking, Conversation, Message, InventoryItem

def dashboard_data(request):
    today = date.today()

    today_bookings = Booking.objects.filter(start_time__date=today).count()

    unanswered = 0
    for conv in Conversation.objects.all():
        if not Message.objects.filter(conversation=conv, sender="staff").exists():
            unanswered += 1

    low_stock = InventoryItem.objects.filter(
        quantity__lte=models.F('low_threshold')
    ).count()

    return JsonResponse({
        "today_bookings": today_bookings,
        "unanswered_conversations": unanswered,
        "low_stock_alerts": low_stock
    })

def inbox(request):
    return render(request, "workspace/inbox.html")


def get_conversations(request):
    from .models import Conversation, Message

    data = []

    for conv in Conversation.objects.all():
        has_alert = Message.objects.filter(
            conversation=conv,
            content__icontains="low stock"
        ).exists()

        data.append({
            "id": conv.id,
            "contact": conv.contact.name,
            "alert": has_alert
        })

    return JsonResponse(data, safe=False)



def get_messages(request, conv_id):
    from .models import Message
    messages = Message.objects.filter(conversation_id=conv_id)

    data = []
    for msg in messages:
        data.append({
            "sender": msg.sender,
            "content": msg.content
        })

    return JsonResponse(data, safe=False)

def send_reply(request):
    from django.views.decorators.csrf import csrf_exempt


from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def send_reply(request):
    if request.method == "POST":
        body = json.loads(request.body)
        conv_id = body.get("conversation_id")
        content = body.get("content")

        from .models import Message

        Message.objects.create(
            conversation_id=conv_id,
            sender="staff",
            channel="email",
            content=content
        )

        return JsonResponse({"status": "sent"})


def get_bookings(request):
    from .models import Booking

    data = []

    for b in Booking.objects.all().order_by("start_time"):
        data.append({
            "id": b.id,
            "customer": b.contact.name,
            "service": b.service.name,
            "time": b.start_time.strftime("%Y-%m-%d %H:%M"),
            "status": b.status
        })

    return JsonResponse(data, safe=False)

@csrf_exempt
def update_booking_status(request):
    import json
    from .models import Booking

    if request.method == "POST":
        body = json.loads(request.body)
        booking_id = body.get("booking_id")
        status = body.get("status")

        booking = Booking.objects.get(id=booking_id)
        booking.status = status
        booking.save()

        return JsonResponse({"status": "updated"})


def seed_demo(request):
    from .models import (
        Workspace, Contact, Conversation, Message,
        Service, Booking, InventoryItem
    )
    from django.utils import timezone
    from datetime import timedelta

    # 🧹 CLEAR OLD DATA FIRST
    Booking.objects.all().delete()
    Message.objects.all().delete()
    Conversation.objects.all().delete()
    Contact.objects.all().delete()
    Service.objects.all().delete()
    InventoryItem.objects.all().delete()
    Workspace.objects.all().delete()

    # 🚀 Now create fresh demo workspace
    ws = Workspace.objects.create(
        name="Demo Clinic",
        address="Mumbai",
        timezone="Asia/Kolkata",
        contact_email="demo@test.com",
        is_active=True
    )

    service = Service.objects.create(
        workspace=ws,
        name="Consultation",
        duration_minutes=60,
        location="Office"
    )

    # 1️⃣ Unanswered Inquiry
    rahul = Contact.objects.create(workspace=ws, name="Rahul")
    conv1 = Conversation.objects.create(workspace=ws, contact=rahul)
    Message.objects.create(
        conversation=conv1,
        sender="customer",
        channel="email",
        content="Hi, I’d like to know your availability."
    )

    # 2️⃣ Confirmed Booking
    priya = Contact.objects.create(workspace=ws, name="Priya")
    conv2 = Conversation.objects.create(workspace=ws, contact=priya)
    Booking.objects.create(
        workspace=ws,
        service=service,
        contact=priya,
        start_time=timezone.now() + timedelta(hours=3)
    )

    # 3️⃣ Low Stock Scenario
    arjun = Contact.objects.create(workspace=ws, name="Arjun")
    conv3 = Conversation.objects.create(workspace=ws, contact=arjun)
    Booking.objects.create(
        workspace=ws,
        service=service,
        contact=arjun,
        start_time=timezone.now() + timedelta(hours=5)
    )

    item = InventoryItem.objects.create(
        workspace=ws,
        name="Medical Gloves",
        quantity=2,
        low_threshold=3
    )

    Message.objects.create(
        conversation=conv3,
        sender="system",
        channel="email",
        content="⚠ Low stock alert: Medical Gloves is below threshold!"
    )

    # 4️⃣ Completed Booking
    sneha = Contact.objects.create(workspace=ws, name="Sneha")
    conv4 = Conversation.objects.create(workspace=ws, contact=sneha)
    Booking.objects.create(
        workspace=ws,
        service=service,
        contact=sneha,
        start_time=timezone.now() - timedelta(hours=2),
        status="completed"
    )

    return JsonResponse({"status": "fresh demo data created"})
