from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message


@login_required
def conversation_view(request, user_id):
    """Optimized view to fetch conversation between current user and another user"""
    messages = (
        Message.objects.filter(sender=request.user, receiver_id=user_id)
        .select_related("sender", "receiver", "parent_message")   # ✅ optimize FKs
        .prefetch_related("replies")                             # ✅ avoid N+1
        .order_by("timestamp")
    )
    return render(request, "messaging/conversation.html", {"messages": messages})


def get_message_thread(message):
    """Recursive helper to fetch threaded replies"""
    return {
        "message": message,
        "replies": [get_message_thread(reply) for reply in message.replies.all()]
    }


@login_required
def message_thread_view(request, message_id):
    """Fetch a message and its threaded replies recursively"""
    message = get_object_or_404(
        Message.objects.select_related("sender", "receiver", "parent_message")
        .prefetch_related("replies"),
        pk=message_id
    )
    thread = get_message_thread(message)
    return render(request, "messaging/thread.html", {"thread": thread})


@login_required
def unread_inbox(request):
    """Display unread messages for the logged-in user"""
    unread_messages = Message.unread.unread_for_user(request.user)
    return render(request, "messaging/unread_inbox.html", {"messages": unread_messages})
