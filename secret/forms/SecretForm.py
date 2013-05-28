#coding=utf-8
from django import forms
from captcha.fields import CaptchaField
from secret.models import Secret
from django.contrib.auth.models import AnonymousUser

class SecretForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SecretForm, self).__init__(*args, **kwargs)
    
    content = forms.CharField(max_length=140,
                             widget=forms.Textarea(attrs={'class': 'span12',
                                                          'rows': '6'}))
    is_public = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    is_anony  = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    captcha = CaptchaField()

    def clean_secret(self):
        content = self.cleaned_data['content']
        if len(content)>140:
            raise forms.ValidationError("您的秘密太长了...")

    def save(self):
        is_anony = self.cleaned_data['is_anony']
        is_public = self.cleaned_data['is_public']
        content = self.cleaned_data['content']

        if is_anony or not self.user.is_authenticated():
            new_secret = Secret(content = content,
                            is_public = is_public)
        else:
            new_secret = Secret(author = self.user,
                            content = content,
                            is_public = is_public)
        new_secret.save()
        return new_secret

