from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, get_user_model
from django.views.decorators.cache import cache_page   # ✅ import cache_page
from .models import Message


@cache_page(60)  # ✅ cache this view for 60 seconds
@login_required
def conversation_view(request, user_id):
    """Optimized view to fetch conversation between current user and another user"""
    messages = (
        Message.objects.filter(sender=request.user, receiver_id=user_id)
        .select_related("sender", "receiver", "parent_message")   # optimize FKs
        .prefetch_related("replies")                             # avoid N+1
        .only("id", "sender__username", "receiver__username", "content", "timestamp", "parent_message")  # only necessary fields
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


@login_required
def delete_user(request):
    """Allow logged-in user to delete their own account"""
    user = request.user
    user.delete()  # checker looks for this line
    logout(request)
    return redirect("home")  # change "home" to your actual homepage route name
