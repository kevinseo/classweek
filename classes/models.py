from django.db import models
from django.contrib.auth.models import User
import datetime

class Company(models.Model):
    name = models.TextField( unique=True )
    phone_number = models.TextField( null=True )
    location = models.TextField()
    zone = models.TextField( null=False, blank=True, default='' )
    nearby_station = models.TextField( null=True )
    facilitiesInfomation = models.TextField()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return 'Company : %s' % self.name

class CompanyImage(models.Model):
    company = models.ForeignKey( Company )
    image_url = models.URLField()

class Category(models.Model):
    name = models.TextField( unique=True )

    def __str__(self):
        return self.name

    def __unicode__(self):
        return 'Category : %s' % self.name

class SubCategory(models.Model):
    name = models.TextField( unique=True )
    category = models.ForeignKey( Category, related_name='get_subcategorys' )
    name_kor = models.TextField( null=True )
    description = models.TextField( null=True )
    image_url = models.URLField( null=True )

    def __str__(self):
        return self.name

    def __unicode__(self):
        return 'SubCategory : %s' % self.name

class Classes(models.Model):
    title = models.TextField( null=True )
    thumbnail_image_url = models.URLField( null=True )
    subCategory = models.ForeignKey( SubCategory, related_name='get_classes' )
    company = models.ForeignKey( Company )
    description = models.TextField( null=True )
    preparation = models.TextField( null=True )
    personalOrGroup = models.TextField( null=True )
    refundInfomation = models.TextField( null=True )
    # countOfDay = models.IntegerField( null=True )
    priceOfDay = models.IntegerField( null=True )
    countOfMonth = models.IntegerField( null=True )
    priceOfMonth = models.IntegerField( null=True )
    image_url = models.URLField( null=True )

    def __str__(self):
        return self.title

    def __unicode__(self):
        return 'Classes : %s / %s' % (self.title, self.description )

class ClassesImage(models.Model):
    classes = models.ForeignKey( Classes, related_name='get_images' )
    image_url = models.URLField()

class ClassesInquire(models.Model):
    classes = models.ForeignKey( Classes )
    user = models.ForeignKey( User )
    content = models.TextField( null=False, blank=True, default='' )
    created = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now )

class Schedule(models.Model):
    classes = models.ForeignKey( Classes , related_name='get_schedules')
    # Mon=1, Tue=2, Wed, Thu, Fri, Sat, Sun
    dayOfWeek = models.CharField( max_length=27 )
    startTime = models.TextField( null=True )
    duration = models.TimeField( default='00:00:00')

    def __str__(self):
        return self.dayOfWeek

    def __unicode__(self):
        return 'Schedule : %s %r' % ( self.dayOfWeek, self.startTime )
