# -*- coding: utf-8 -*-
from google.appengine.ext.db import djangoforms
from courses import models
from django import forms

LANG_CODES=[('en' , 'english'),('zh_CN' , 'CHINESE_SIMPLIFIED'),('zh_TW' , 'CHINESE_TRADITIONAL'),('de' , 'German'),('fr' , 'France')]
REGIONS =[('cn','中国'),('tw','中国台湾'),('hk','中国香港'),('all','All')]
LEVEL =[('fund','fundamental'),('midd','middle'),('adva','advanced')]
COURSE_TYPE =[('simp','simple'),('self','self-dictionary'),('nodi','no-dictionary')]


#class CourseForm(forms.Form):
#    lang_code=forms.CharField(widget=forms.Select(choices=LANG_CODES))

class CourseForm(djangoforms.ModelForm):
    lang_code=forms.CharField(widget=forms.Select(choices=LANG_CODES))
    region_code=forms.CharField(widget=forms.Select(choices=REGIONS))
    level_code=forms.CharField(widget=forms.Select(choices=LEVEL))
    type_code=forms.CharField(widget=forms.Select(choices=COURSE_TYPE))
    class Meta:
        model=models.Course
        exclude = ('content_blob','content','creator','ready','content_count','rating')
        
class ContentForm(djangoforms.ModelForm):
    class Meta:
        model=models.Course
        fields = ('content')
  
class EditContentForm(forms.Form):
    content=forms.CharField(required=True,widget=forms.Textarea(attrs={'rows':20, 'cols':40}))
    