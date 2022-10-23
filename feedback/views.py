from django.core.mail import send_mail, EmailMessage, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, EmailListForm
from .models import Contact, EmailList
from .tasks import send_bcc_task

def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, 'contactform@dpp-connect.org', ['admin@dpp-connect.org'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "email.html", {'form': form})

@login_required(login_url = '/accounts/login/')
def emailListView(request, list_pk):
    mylist = get_object_or_404(EmailList, pk=list_pk)
    if request.method == 'GET':
        form = EmailListForm()
    else:
        form = EmailListForm(request.POST, request.FILES)
        if form.is_valid():
            subject = "["+mylist.name +"] "+ form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                #mail = EmailMessage(subject, message, 'chair@dpp-connect.org', bcc=mylist.list())
                #mail.send()
                send_bcc_task.delay(subject,message,mylist.list())
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "emaillist.html", {'form': form, 'list':mylist})


def successView(request):
    return HttpResponse('Success! Thank you for your message.')
