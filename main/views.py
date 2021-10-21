from django.shortcuts import render, get_object_or_404
from django.views import generic
from main.models import JobPosting, Person, Meeting, Panel, TownHall, StudentDay
from main.models import OrgsList,PanelMember, MemberAtLarge, Award
from main.models import ResourcePage, Resource
from main.models import HTMLBlock
from django.utils import timezone
import feedparser 

def index(request):
    """View function for home page of site."""
    
    myblock,created = HTMLBlock.objects.get_or_create(name="home-about")
    if created:
        myblock.text = "<p>Placeholder</p>"
        myblock.save()
    awards = Award.objects.filter(duedate__gte=timezone.now()).order_by('duedate')
    meetings = Meeting.objects.all().order_by('-startdate')
    orglist,_ = OrgsList.objects.get_or_create(title="CONNECT")
    jobs = JobPosting.objects.all().order_by('-pubdate')
    
    try:
        context={"about":myblock,"awards":awards,'jobs':jobs,
            "current":meetings[0],"meetings":meetings[1:],'orgs':orglist,}
    except:
        context={"about":myblock,"jobs":jobs,"awards":awards,
            "current":None,"meetings":None,'orgs':orglist}

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'main/index.html', context=context)

def about(request):
    orgs = OrgsList.objects.get(title="CONNECT")
    context={'orgs':orgs}
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'main/about.html', context=context)

def awards(request):
    awards = Award.objects.all().order_by('duedate')
    myblock,_ = HTMLBlock.objects.get_or_create(name="awards-about")
    try:
        last = awards.reverse()[0].last_modified
    except:
        last = None

    context={'awards':awards, 'awards-about':myblock, 'last':last}
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'main/awards.html', context=context)

def students(request):
    pg,_ = ResourcePage.objects.get_or_create(title="Students")
    awards = Award.objects.filter(careerstage__lte=1).order_by('duedate')
    context={"page":pg, "awards":awards}
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'main/students.html', context=context)

def postdocs(request):
    pg,_ = ResourcePage.objects.get_or_create(title="Postdocs")
    awards = Award.objects.filter(careerstage=2).order_by('duedate')
    context={"page":pg, "awards":awards}
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'main/postdocs.html', context=context)

def earlycareer(request):
    pg,_ = ResourcePage.objects.get_or_create(title="Early Career")
    awards = Award.objects.filter(careerstage=3).order_by('duedate')
    context={"page":pg, "awards":awards}
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'main/earlycareer.html', context=context)


def meeting(request):
    meetings = Meeting.objects.all().order_by('-startdate')
    try:
        context={"current":meetings[0],"old":meetings}
    except:
        context={"current":None,"old":[]}
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'main/meeting.html', context=context)

class PersonDetailView(generic.DetailView):
    model = Person

def MeetingDetailView(request,pk):
    current = get_object_or_404(Meeting,pk=pk)
    meetings = Meeting.objects.all().order_by('-startdate')
    context={"current":current,"old":meetings}
    # Render the HTML template with the data in the context variable
    return render(request, 'main/meeting.html', context=context)
