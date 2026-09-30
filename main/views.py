from main.models import Experience, Education
from main.forms import EducationForm
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
import os
import datetime
SECRET_CODE = os.environ.get("PORTFOLIO_SECRET_CODE")

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Callista Putri Anjola",
        "npm": "2506603740",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "I am a second-year Information Systems student at Universitas Indonesia who is "
            "passionate about learning technology and making a social impact. I am motivated to "
            "develop practical skills, excited to take on new challenges, and committed to "
            "contributing effectively in teamwork. I am ready to learn and grow with an open mind and a willingness to improve."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Callista Putri Anjola",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    institution_query = request.GET.get("institution", "").strip()
    is_editor = request.user.groups.filter(name="Editor").exists()

    context = {
        "name": "Callista Putri Anjola",
        "institution_query": institution_query,
        "is_editor": is_editor,
        "form": EducationForm(),
    }

    return render(request, "education.html", context)

def get_education_json(request):
    institution_query = request.GET.get("institution", "").strip()
    education = Education.objects.prefetch_related("starred_by").all()

    if institution_query:
        education = education.filter(
            institution__icontains=institution_query
        )

    data = []

    for item in education:
        starred_users = item.starred_by.all()

        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )

        starred_by_names = ", ".join(
            [user.username for user in starred_users]
        )

        data.append({
            "pk": str(item.id),
            "fields": {
                "institution": item.institution,
                "field_of_study": item.field_of_study,
                "started": item.started.isoformat(),
                "ended": item.ended.isoformat() if item.ended else None,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        if form.cleaned_data["password"] != SECRET_CODE:
            form.add_error("password", "Kode salah.")
        else:
            form.save()
            messages.success(request, "Pendidikan baru berhasil ditambahkan")
            return redirect("main:show_education")

    context = {
        "name": "Callista Putri Anjola",
        "form": form,
    }

    return render(request, "educations_form.html", context)

@require_POST
def create_education_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan pendidikan."},
            status=403,
        )

    form = EducationForm(request.POST)

    if form.is_valid():
        education = form.save()

        return JsonResponse(
            {
                "message": "Pendidikan berhasil ditambahkan.",
                "pk": str(education.id),
            },
            status=201,
        )

    return JsonResponse(
        {"errors": form.errors.get_json_data()},
        status=400,
    )


@login_required(login_url="/login/")
def update_education(request, education_id):
    if not (
        request.user.is_superuser 
        or request.user.groups.filter(name="Editor").exists()
    ):
        raise PermissionDenied
    
    education = get_object_or_404(Education, pk=education_id)

    form = EducationForm(
        request.POST or None,
        instance=education
    )

    if request.method == "POST" and form.is_valid():
        if form.cleaned_data["password"] != SECRET_CODE:
            form.add_error("password", "Kode salah.")
        else:
            form.save()
            messages.success(
                request,
                "Pendidikan berhasil diperbarui!"
            )
            return redirect("main:show_education")

    context = {
        "name": "Callista Putri Anjola",
        "form": form,
        "education": education,
    }

    return render(
        request,
        "education_update_form.html",
        context
    )

@login_required(login_url="/login/")
def delete_education(request, education_id):
    if not request.user.is_superuser:
            raise PermissionDenied
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Pendidikan berhasil dihapus!")
        return redirect("main:show_education")

    return redirect("main:show_education")

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Callista Putri Anjola",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Callista Putri Anjola",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
def toggle_star(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        if request.user in education.starred_by.all():
            education.starred_by.remove(request.user)
        else:
            education.starred_by.add(request.user)
    return redirect("main:show_education")