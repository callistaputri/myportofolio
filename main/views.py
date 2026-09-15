from main.models import Experience, Education
from main.forms import EducationForm
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.core import serializers
from django.http import HttpResponse
import os
SECRET_CODE = os.environ.get("PORTFOLIO_SECRET_CODE")

def show_main(request):
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
        "experience_list": Experience.objects.all(),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Callista",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    request.META["HTTP_X_PORTFOLIO_SECRET"] = SECRET_CODE
    json_response = get_education_json(request)

    education = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )

    education = [item.object for item in education]
    institution_query = request.GET.get("institution", "").strip()

    context = {
        "name": "Callista Putri Anjola",
        "education_list": education,
        "institution_query": institution_query,
    }
    return render(request, "education.html", context)

def get_education_json(request):
    secret_code = request.headers.get("X-Portfolio-Secret")

    if secret_code != SECRET_CODE:
        return HttpResponse(
            "Unauthorized",
            status=401,
        )
    
    institution_query = request.GET.get("institution", "").strip()
    education = Education.objects.all()

    if institution_query:
        education = education.filter(
            institution__icontains=institution_query
        )

    education_json = serializers.serialize("json", education)
    return HttpResponse(education_json, content_type="application/json")

def create_education(request):
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

def delete_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Pendidikan berhasil dihapus!")
        return redirect("main:show_education")

    return redirect("main:show_education")