from django.forms import ModelForm, TextInput, DateInput

from main.models import Education

from django import forms

class EducationForm(ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs= {
                "placeholder": "Masukkan kode rahasia",
            }
        ),
    )
    class Meta:
        model = Education
        fields = [
            "institution",
            "field_of_study",
            "started",
            "ended",
        ]

        labels = {
            "institution": "Universitas Indonesia",
            "field_of_study": "Information Systems",
            "started": "Mulai",
            "ended": "Selesai",
        }

        widgets = {
            "institution": TextInput(
                attrs={
                    "placeholder": "Universitas Indonesia",
                    "maxlength": 255,
                }
            ),
            "field_of_study": TextInput(
                attrs={
                    "placeholder": "Information Systems",
                    "maxlength": 255,
                }
            ),
            "started": DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "ended": DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }