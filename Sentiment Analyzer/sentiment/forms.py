from django import forms

class TweetForm(forms.Form):
    tweet = forms.CharField(
        label='Enter a statement:',
        max_length=1000,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Type any public opinion, comment, or statement...',
            'rows': 8,              
            'style': 'width:100%; font-size:1.1rem;'  
        })
    )