from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from ml_model.train_model import predict_vehicle_count
from .models import PredictionHistory
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('prediction')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def prediction_view(request):
    if request.method == 'POST':
        datetime_str = request.POST['datetime']
        predicted_count = predict_vehicle_count(datetime_str)
        print(f"Predicted count: {predicted_count}")  # Debug
        PredictionHistory.objects.create(
            user=request.user,
            datetime=datetime_str,
            predicted_count=predicted_count
        )
        return render(request, 'prediction.html', {
            'prediction': predicted_count,
            'datetime': datetime_str
        })
    return render(request, 'prediction.html')

def logout_view(request):
    logout(request)
    return redirect('login')