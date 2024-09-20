from django import forms
from django.contrib.auth.forms import UserCreationForm

from storage.models import User, Comment


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter text to search."}
        )
    )


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = (UserCreationForm.Meta.fields
                  + ("first_name", "last_name", "occupation",))


class CommentForm(forms.ModelForm):
    content = forms.TimeInput(attrs={"rows": 2})

    class Meta:
        model = Comment
        fields = ["content"]
        widget = {
            "content": forms.TextInput(
                attrs={
                    "rows": 2,
                    "placeholder": "Enter your comment",
                    "label": ""}
            ),
        }
