from django.forms import ModelForm, TextInput, DateInput
from main.models import Education
from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

class EducationForm(ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
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

    def clean_institution(self):
        institution = strip_tags(
            self.cleaned_data["institution"]
        ).strip()

        if not institution:
            raise ValidationError(
                "Nama institusi tidak boleh hanya berisi tag HTML."
            )

        return institution

    def clean_field_of_study(self):
        return strip_tags(
            self.cleaned_data["field_of_study"]
        ).strip()