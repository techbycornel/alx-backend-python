from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def delete_user(request):
    user = request.user
    user.delete()  # This will trigger the post_delete signal
    return redirect('/')  # redirect to home or login page after deletion
