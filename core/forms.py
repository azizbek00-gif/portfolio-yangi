from django import forms

from .models import Message


class ContactForm(forms.ModelForm):
    # Honeypot: odam ko'rmaydi, botlar to'ldiradi.
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Message
        fields = ["name", "phone", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel", "type": "tel"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "message": forms.Textarea(attrs={"rows": 5}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("website"):
            raise forms.ValidationError("Xabar yuborilmadi.")
        return cleaned

    def clean_message(self):
        text = self.cleaned_data["message"].strip()
        if len(text) < 10:
            raise forms.ValidationError("Xabar kamida 10 ta belgidan iborat bo'lsin.")
        return text
