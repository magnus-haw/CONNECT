from django.db import models
#from djgeojson.fields import PointField,PolygonField
from django.utils import timezone
from ckeditor.fields import RichTextField

# Create your models here.
RESOURCE_TYPES = (
    (0, 'awards'),
    (1, 'career'),
    (2, 'volunteer'),
    (3, 'physics')
)

class Resource(models.Model):
    title = models.CharField(max_length=200)
    description =models.TextField(null=True,blank=True)
    link = models.URLField(blank=True,null=True)
    file = models.FileField(blank=True,null=True)
    category =models.PositiveIntegerField(choices=RESOURCE_TYPES,default=1)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class ResourcePage(models.Model):
    title = models.CharField(max_length=200)
    aboutblock = RichTextField(config_name='myconfig')
    awardblock = RichTextField(config_name='myconfig')
    volunteerblock = RichTextField(config_name='myconfig')
    careerblock = RichTextField(config_name='myconfig')
    resources = models.ManyToManyField(Resource,blank=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class Person(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50,blank=True,null=True)
    position = models.CharField(max_length=200,blank=True,null=True)
    affiliation = models.CharField(max_length=200,blank=True,null=True)
    email = models.EmailField(unique=True,blank=True,null=True)
    otheremail = models.EmailField(blank=True,null=True)
    website = models.URLField(blank=True,null=True)
    ORCID = models.CharField(blank=True,null=True,max_length=50)
    phone = models.CharField(max_length=15,null=True,blank=True)
    description =models.TextField(null=True,blank=True)
    image = models.ImageField(blank=True, null=True)
    resources = models.ManyToManyField(Resource,blank=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        """String for representing the Model object."""
        if self.middlename is None:
            return self.firstname + ' '+ self.lastname
        else:
            return self.firstname +' '+ self.middlename[0]+ '. ' + self.lastname

    class Meta:
        get_latest_by = 'last_modified'

class OrgsList(models.Model):
    title = models.CharField(max_length=25)
    chair = models.ForeignKey(Person,null=True,on_delete=models.SET_NULL,related_name='chair')
    vicechair = models.ForeignKey(Person,null=True,on_delete=models.SET_NULL,related_name='vicechair')
    pastchair = models.ForeignKey(Person,null=True,on_delete=models.SET_NULL,related_name='pastchair')
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class MemberAtLarge(models.Model):
    title = models.CharField(max_length=25)
    member = models.ForeignKey(Person,on_delete=models.CASCADE)
    org = models.ForeignKey(OrgsList,on_delete=models.CASCADE)

    def __str__(self):
        return self.org.title + ": " + self.title

class Location(models.Model):
    title =  models.CharField(max_length=25)
    street=  models.CharField(max_length=25, null=True,blank=True)
    city  =  models.CharField(max_length=25, null=True,blank=True)
    state =  models.CharField(max_length=25, null=True,blank=True)
    country= models.CharField(max_length=25, null=True,blank=True)
    zipcode= models.CharField(max_length=10, null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title

class StudentDay(models.Model):
    title =  models.CharField(max_length=25)
    date = models.DateField()
    location = models.ForeignKey(Location,blank=True,null=True,on_delete=models.SET_NULL)
    description = models.TextField(null=True,blank=True)
    block0 = RichTextField(blank=True,null=True,config_name='myconfig')
    block1 = RichTextField(blank=True,null=True,config_name='myconfig')
    image = models.ImageField(blank=True, null=True)
    resources = models.ManyToManyField(Resource,blank=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class Panel(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(blank=True, null=True)
    video = models.FileField(blank=True,null=True)
    resources = models.ManyToManyField(Resource,blank=True)

    def __str__(self):
        return self.title

class PanelMember(models.Model):
    panel = models.ForeignKey(Panel, related_name='members', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

class TownHall(models.Model):
    title =  models.CharField(max_length=25)
    date = models.DateField()
    location = models.ForeignKey(Location,blank=True,null=True,on_delete=models.SET_NULL)
    description = models.TextField(null=True,blank=True)
    panel = models.ForeignKey(Panel,blank=True,null=True,on_delete=models.SET_NULL)
    block0 = RichTextField(blank=True,null=True,config_name='myconfig')
    block1 = RichTextField(blank=True,null=True,config_name='myconfig')
    image = models.ImageField(blank=True, null=True)
    resources = models.ManyToManyField(Resource,blank=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class Meeting(models.Model):
    title =  models.CharField(max_length=25)
    startdate = models.DateField()
    enddate = models.DateField()
    location = models.ForeignKey(Location,blank=True,null=True,on_delete=models.SET_NULL)
    townhall = models.ForeignKey(TownHall,blank=True,null=True,on_delete=models.SET_NULL)
    studentday = models.ForeignKey(StudentDay,blank=True,null=True,on_delete=models.SET_NULL)
    website = models.URLField(blank=True,null=True)
    last_modified = models.DateField(auto_now=True)
    description =models.TextField(null=True,blank=True)

    def __str__(self):
        return self.title

CAREER_STAGES = (
    (0, 'Undergrad'),
    (1, 'Graduate'),
    (2, 'Postdoc'),
    (3, 'Early career')
)

class Award(models.Model):
    title =  models.CharField(max_length=100)
    careerstage = models.PositiveIntegerField(choices=CAREER_STAGES,default=1)
    duedate = models.DateField(null=True, blank=True)
    description = RichTextField(config_name='myconfig')
    howtoapply = models.URLField(blank=True,null=True)
    contact = models.ForeignKey(Person,blank=True,null=True,on_delete=models.SET_NULL)
    number = models.PositiveIntegerField(blank=True, null=True)
    amount = models.PositiveIntegerField(blank=True, null=True)
    visible = models.BooleanField(default=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class HTMLBlock(models.Model):
    name = models.CharField(max_length=100)
    text = RichTextField(config_name='myconfig')
    date = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class JobPosting(models.Model):
    title = models.CharField(max_length=300)
    link = models.URLField(unique=True)
    description = models.TextField(null=True, blank=True)
    pubdate = models.DateField(null=True)

    def __str__(self):
        return self.title
