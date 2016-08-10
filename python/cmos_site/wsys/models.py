from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from django import forms
from django.forms import ModelForm
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

CATE_CHOICES = (
    ('c', 'c'),
    ('python', 'python'),
    ('perl', 'perl'),
    ('lisp', 'lisp'),
    ('html', 'html'),
    ('common', 'common')
)

class Article(models.Model):
    pub_date = models.DateTimeField('date published')
    headline = models.CharField(max_length=200)
    content = RichTextUploadingField()
    reporter = models.CharField(max_length=50)
    reviser = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=CATE_CHOICES)
    def __str__(self):
        return self.reporter+'__'+self.headline

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['category', 'headline', 'content']
        exclude = ['pub_date', 'reporter']
        widgets = {
            'headline': forms.TextInput(attrs={'size': '80'}),
        }
