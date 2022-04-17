from django.shortcuts import render, get_object_or_404
from django.views import generic
from main.models import JobPosting, Person, Meeting, Panel, TownHall, StudentDay
from main.models import OrgsList,PanelMember, MemberAtLarge, Award
from main.models import ResourcePage, Resource
from main.models import HTMLBlock
from django.utils import timezone
from django.utils.html import format_html
import feedparser 

import django_filters
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
import django_tables2 as tables
from django_tables2 import A


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


class TruncatedTextColumn(tables.Column):
    '''A Column to limit to 100 characters and add an ellipsis'''
    def render(self, value):
        if len(value) > 102:
            return value[0:99] + '...'
        return str(value)

class JobFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = JobPosting
        fields = ['title', 'description']

class JobTable(tables.Table):
    title = tables.Column()
    description = TruncatedTextColumn(accessor=A('description'))
    class Meta:
        model = JobPosting
        template_name = "django_tables2/bootstrap.html"
        fields = ["title",'description','pubdate']
    
    def render_title(self, value, record):
        return format_html("<a href={}>{}</a>", record.link, value)

class JobListView(SingleTableMixin, FilterView):
    table_class = JobTable
    model = JobPosting
    template_name = "main/joblist.html"
    filterset_class = JobFilter


# def joblist(request):
#     """View function for joblist page of site."""
    
#     jobs = JobPosting.objects.all().order_by('-pubdate')
    
#     context={"jobs":jobs}

#     # Render the HTML template index.html with the data in the context variable
#     return render(request, 'main/joblist.html', context=context)