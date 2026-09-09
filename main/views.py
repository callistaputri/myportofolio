from django.shortcuts import render

from main.models import Experience


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