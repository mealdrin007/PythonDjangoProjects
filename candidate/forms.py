from django import forms
from candidate.models import CandidateProfile


class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        exclude = ("user",)
        widgets={
            "profile_pic":forms.FileInput(attrs={"class":"form-control"}),
            "qualification":forms.TextInput(attrs={"class":"form-control"}),
            "age":forms.NumberInput(attrs={"class":"form-control"}),
            "skills":forms.TextInput(attrs={"class":"form-control"}),
            "cv":forms.FileInput(attrs={"class":"form-control"}),
        }