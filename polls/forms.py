from django import forms
from django.core.exceptions import ValidationError

from polls.models import Question


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100, required=True, help_text="test")


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class QuestionForm(forms.Form):
    # question_text = models.CharField(max_length=200)
    # pub_date = models.DateTimeField("date published")
    question_text = forms.CharField(max_length=200)
    # pub_date = forms.DateTimeField()

    def clean(self):
        super().clean()
        if self.cleaned_data.get("question_text") == "Pavlo":
            raise ValidationError("question_text couldn't be 'Pavlo'")

    def clean_question_text(self):
        if self.cleaned_data.get("question_text") == "Sasha":
            raise ValidationError("question_text couldn't be 'Sasha'")
        return self.cleaned_data.get("question_text")


class QuestionModelForm(forms.ModelForm):
    question_text = forms.CharField(max_length=200)

    class Meta:
        model = Question
        fields = ["question_text"]

    def clean(self):
        super().clean()
        if self.cleaned_data.get("question_text") == "Pavlo":
            raise ValidationError("question_text couldn't be 'Pavlo'")

    def clean_question_text(self):
        if self.cleaned_data.get("question_text") == "Sasha":
            raise ValidationError("question_text couldn't be 'Sasha'")
        return self.cleaned_data.get("question_text")
