from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import ModelForm,TextInput,Textarea
from django.contrib.auth.models import User
# Create your models here.

class Settings(models.Model):

    STATUS=(

        ('True','True'),
        ('False','False')
        )

    title=models.CharField(max_length=150)

    titlepage1=models.CharField(max_length=150)
    titlePageAccueil=models.CharField(max_length=150)
    titlePageHowitworks=models.CharField(max_length=150)
    titlePageService=models.CharField(max_length=150)
    titlePageContact=models.CharField(max_length=150)

    descriptionPage1=RichTextUploadingField(blank=True)
    descriptionPageAccueil=RichTextUploadingField(blank=True)
    descriptionPageHowitworks=RichTextUploadingField(blank=True)
    descriptionAboutus=RichTextUploadingField(blank=True)
    descriptionPageContact=RichTextUploadingField(blank=True)

    descriptionFacbook=RichTextUploadingField(blank=True)
    descriptionTwitter=RichTextUploadingField(blank=True)
    descriptionYoutube=RichTextUploadingField(blank=True)

    company=models.CharField(max_length=50)
    address=models.CharField(blank=True,max_length=100)
    phone1=models.CharField(blank=True,max_length=15)
    phone2=models.CharField(blank=True,max_length=50)
    fax=models.CharField(blank=True,max_length=15)
    email1=models.CharField(blank=True,max_length=50)
    email2=models.CharField(blank=True,max_length=50)
    

    facbook=models.CharField(blank=True,max_length=50)
    instagram=models.CharField(blank=True,max_length=50)
    twitter=models.CharField(blank=True,max_length=50)
    youtube=models.CharField(blank=True,max_length=50)
    linkedin=models.CharField(blank=True,max_length=50)

    
    reference=RichTextUploadingField(blank=True)
    status=models.CharField(max_length=10,choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
        
    def __str__ (self):
        return self.title        

        


class ContactMessage(models.Model):

    STATUS=(

        ('New','New'),
        ('Read','Read'),
        ('Closed','Closed')
        )

    
    name=models.CharField(blank=True,max_length=20)
    email=models.CharField(blank=True,max_length=50)
    subject=models.CharField(blank=True,max_length=50)
    message=models.CharField(blank=True,max_length=255)
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    note=models.CharField(blank=True,max_length=100)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
  
    def __str__ (self):
        return self.name        


class ContactForm(ModelForm):

    class Meta:
        model=ContactMessage
        fields=['name','email','subject','message']
        widgets={
            'name':TextInput(attrs={'class':'input','palaceholder':'Name & Surname'}),
            'subject':TextInput(attrs={'class':'input','palaceholder':'subject'}),
            'email':TextInput(attrs={'class':'input','palaceholder':'Email Address'}),
            'message':Textarea(attrs={'class':'input','palaceholder':'your message','rows':'5'}),
        }



class AccessTokenFB(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    token= models.CharField(max_length=200,blank=True)

    def __str__ (self):
        return self.token

