from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking, Conversation, Message
from .models import InventoryItem


@receiver(post_save, sender=Booking)
def booking_confirmation(sender, instance, created, **kwargs):
    if created:
        # get or create conversation
        conv, _ = Conversation.objects.get_or_create(
            workspace=instance.workspace,
            contact=instance.contact
        )

        Message.objects.create(
            conversation=conv,
            sender="system",
            channel="email",
            content=f"Your booking for {instance.service.name} is confirmed!"
        )



@receiver(post_save, sender=InventoryItem)
def low_stock_alert(sender, instance, **kwargs):
    if instance.quantity <= instance.low_threshold:
        # Create or get a conversation for alerts
        # We’ll send it to the first OWNER in workspace
        from django.contrib.auth.models import User
        from .models import UserProfile, Conversation, Message

        owner_profile = UserProfile.objects.filter(
            workspace=instance.workspace,
            role="OWNER"
        ).first()

        if owner_profile:
            # Create fake contact for owner alerts (if needed)
            contact = owner_profile.user

            # We create a system conversation for alerts
            conv, _ = Conversation.objects.get_or_create(
                workspace=instance.workspace,
                contact=instance.workspace.contact_set.first()
            )

            Message.objects.create(
                conversation=conv,
                sender="system",
                channel="email",
                content=f"⚠ Low stock alert: {instance.name} is below threshold!"
            )
