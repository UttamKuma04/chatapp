from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt


def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("email", "").strip()  # username or phone
        password = request.POST.get("password", "")

        user = None
        try:
            u = User.objects.get(username=identifier)
            user = authenticate(request, username=u.username, password=password)
        except User.DoesNotExist:
            try:
                u = User.objects.get(email=identifier)  # phone stored in email
                user = authenticate(request, username=u.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            auth_login(request, user)  # call Django's login
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, "login.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        phone_number = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirmation = request.POST.get("confirmation", "")

        if not username or not phone_number or not password:
            messages.error(request, "All fields are required.")
        elif password != confirmation:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
        elif User.objects.filter(email=phone_number).exists():  # using email field for phone
            messages.error(request, "Phone number is already registered.")
        else:
            # Create the user
            user = User.objects.create_user(
                username=username,
                email=phone_number,  # storing phone_number in email field
                password=password
            )
            user.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")

    return render(request, "register.html")


@login_required
def home(request):
    return render(request, "base.html")

# --- ADD THIS NEW VIEW ---
@login_required # Protect the upload view
@csrf_exempt # Use this for simplicity; consider proper CSRF setup for production
def upload_file_view(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            uploaded_file = request.FILES['file']
            
            # Save the file to your media directory
            path = default_storage.save(f'chat_files/{uploaded_file.name}', ContentFile(uploaded_file.read()))
            file_url = default_storage.url(path)

            # Prepare the data in the format your JavaScript expects
            message_data = {
                'message': request.POST.get('message', ''),
                'file_url': file_url,
                'file_name': uploaded_file.name,
                'file_type': uploaded_file.content_type,
                'file_size': uploaded_file.size,
            }

            # Return a JSON response on success
            return JsonResponse({'status': 'success', 'message_data': message_data})

        except Exception as e:
            # Return a JSON error if something goes wrong
            return JsonResponse({'status': 'error', 'error': str(e)}, status=500)

    # Return a JSON error for bad requests (e.g., not a POST request)
    return JsonResponse({'status': 'error', 'error': 'Invalid request'}, status=400)
