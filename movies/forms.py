from django import forms
from .models import Movie,Comment

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            'title',
            'poster',
            'description',
            'release_date',
            'actors',
            'rating',
            'category',
            'trailer_url',
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']