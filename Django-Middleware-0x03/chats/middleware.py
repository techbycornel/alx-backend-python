import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='requests.log', level=logging.INFO)


class RequestLoggingMiddleware:
    """Logs every request with timestamp, user, and path."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if hasattr(request, "user") and request.user.is_authenticated else "Anonymous"
        log_msg = f"{datetime.datetime.now()} - User: {user} - Path: {request.path}\n"

        with open("requests.log", "a") as f:
            f.write(log_msg)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware(MiddlewareMixin):
    """Restricts access to chats between 9PM and 6AM."""

    def process_request(self, request):
        current_time = datetime.now().time()
        if current_time >= time(21, 0) or current_time <= time(6, 0):
            return HttpResponseForbidden("Chat access restricted at this time.")


class OffensiveLanguageMiddleware(MiddlewareMixin):
    """
    Limits number of chat messages from an IP address.
    Example: max 5 messages per minute.
    """

    ip_message_counts = {}

    def process_request(self, request):
        if request.method == "POST" and "messages" in request.path:
            ip = self.get_client_ip(request)
            now = datetime.now()
            window = self.ip_message_counts.get(ip, [])
            # Remove timestamps older than 1 minute
            window = [t for t in window if (now - t).seconds < 60]
            if len(window) >= 5:
                return HttpResponseForbidden("Message limit exceeded. Try again later.")
            window.append(now)
            self.ip_message_counts[ip] = window

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolepermissionMiddleware:
    """Middleware to enforce role-based access control."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Example role check: requires 'admin' or 'moderator'
        user = getattr(request, "user", None)

        if user and user.is_authenticated:
            role = getattr(user, "role", None)  # assumes your User model has a 'role' field
            if role not in ["admin", "moderator"]:
                return JsonResponse({"error": "Forbidden: insufficient role"}, status=403)

        return self.get_response(request)
