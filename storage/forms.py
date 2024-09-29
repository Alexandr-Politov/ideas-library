from django import forms
from django.contrib.auth.forms import UserCreationForm

from storage.models import User, Comment, Idea, Category


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
        labels = {"content": ""}
        widgets = {
            "content": forms.TextInput(
                attrs={
                    "rows": 2,
                    "placeholder": "Enter your comment",}
            ),
        }


class IdeaForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Idea
        fields = "__all__"
        exclude = ["author"]
