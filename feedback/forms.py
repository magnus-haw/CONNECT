# sendemail/forms.py
from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":50}), required=True)

class EmailListForm(forms.Form):
    subject = forms.CharField(label='Subject', required = True )
    message = forms.CharField(label='Message body', widget=forms.Textarea, required = True )

