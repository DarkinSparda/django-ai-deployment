from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import BlogPost
import json
import time

# API functions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from .youtube import yt_title, get_transcription, get_transcription_whisper
from ai.blog_generator import generate_blog_from_transcript
# Create your views here.

@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def generate_blog(request):
    # Accepts POST methods only
    if request.method == 'POST':

        try:
            data = json.loads(request.body)
            yt_link = data.get('link')

            if not yt_link:
                return JsonResponse({'error': "Missing 'link' field in request"}, status=400)

        except Exception as e:
            print(f"Error parsing request: {e}")
            return JsonResponse({'error': f"Invalid data sent: {str(e)}"}, status=400)


        try:
            start = time.time()
            title = yt_title(yt_link)
            transcription = get_transcription(yt_link)
            time_to_get_text = time.time() - start
            print("GOT TRANSCRIPTION")

            if not transcription:
                return JsonResponse({"error": "Failed to get transcript from YouTube video"}, status=500)

            generation_result = generate_blog_from_transcript(transcription)
            print("GOT GENERATED RESULTS")
            blog_content = generation_result['generated_text']
            blog_model = generation_result['model']

        except Exception as e:
            print(f"Error during blog generation: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({"error": f"Failed to generate blog: {str(e)}"}, status=500)
        
        time_to_get_summary = time.time() - start - time_to_get_text

        blog_obj = BlogPost.objects.create(
            user=request.user,
            youtube_title=title,
            youtube_link=yt_link,
            transcript=transcription,
            generated_content=blog_content,
            model_used=blog_model,
            time_to_generate=round(time_to_get_text, 3),
            time_to_summarize=round(time_to_get_summary, 3),
        )
        blog_obj.save()

        print("to save object it took: ", round(time_to_get_summary, 3))

        return JsonResponse({'title': title,'content': blog_content, 'time_taken': round(time_to_get_summary, 3)})
    else:
        return JsonResponse({'error': "Invalid request method"}, status=405)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid username or password'
            ctx = {"error_message": error_message}
            return render(request, 'login.html', ctx)
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']
        
        if password == repeatPassword:
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )
                user.save()
                login(request, user)
                return redirect("/")
            except:
                error_message = "Error creating account"
                ctx = {"error_message": error_message}
                return render(request, 'signup.html', ctx)
        else:
            error_message = 'Password Dont match'
            ctx = {"error_message": error_message}
            return render(request, 'signup.html', ctx)

    return render(request, 'signup.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('/')
