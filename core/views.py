# core/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import AcademicYear, Semester, ExamType, Resource

# Custom login view (handles already-logged-in users)
def login_view(request):
    # If already logged in → go home
    if request.user.is_authenticated:
        return redirect('home')
    
    # Handle redirect after login
    next_url = request.GET.get('next') or request.POST.get('next') or 'home'
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                # Redirect to 'next' or home
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {
        'form': form,
        'next': request.GET.get('next', '')  # Pass to template (optional)
    })
# Home: show all years
def home(request):
    years = AcademicYear.objects.all()
    return render(request, 'core/home.html', {'years': years})

# Year detail: show semesters
def year_detail(request, year_num):
    year = get_object_or_404(AcademicYear, year_number=year_num)
    semesters = year.semesters.all()
    return render(request, 'core/year_detail.html', {
        'year': year,
        'semesters': semesters
    })

# Semester detail: show exam types
def semester_detail(request, year_num, sem_num):
    year = get_object_or_404(AcademicYear, year_number=year_num)
    semester = get_object_or_404(Semester, year=year, semester_number=sem_num)
    exam_types = ExamType.objects.all()
    return render(request, 'core/semester_detail.html', {
        'semester': semester,
        'exam_types': exam_types
    })

# Premium check helper
def premium_required(user):
    return user.is_authenticated and user.profile.is_premium

# Custom decorator that combines login + premium check with clean redirects
def premium_required_view(view_func):
    @login_required(login_url='/login/')
    def _wrapped_view(request, *args, **kwargs):
        if not premium_required(request.user):
            return redirect('upgrade')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Apply the combined decorator
@premium_required_view
def resource_list(request, year_num, sem_num, exam_name):
    year = get_object_or_404(AcademicYear, year_number=year_num)
    semester = get_object_or_404(Semester, year=year, semester_number=sem_num)
    exam = get_object_or_404(ExamType, name__iexact=exam_name.upper())
    resources = Resource.objects.filter(semester=semester, exam_type=exam)
    return render(request, 'core/resource_list.html', {
        'semester': semester,
        'exam': exam,
        'resources': resources
    })

# Auth views (unchanged)
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created! You now have free access.")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'core/profile.html')

@login_required
def upgrade(request):
    return render(request, 'core/upgrade.html')