# -*- coding: utf-8 -*-
from google.appengine.ext.db import djangoforms
from courses import models
from django import forms

LANG_CODES=[('en' , 'English'),('zh_CN' , 'CHINESE_SIMPLIFIED'),('zh_TW' , 'CHINESE_TRADITIONAL'),('de' , 'German'),('fr' , 'France')]
REGIONS =[('cn','中国'),('tw','中国台湾'),('hk','中国香港'),('all','All')]
LEVEL =[('fund','fundamental'),('midd','middle'),('adva','advanced')]
COURSE_TYPE =[('simp','simple'),('self','self-dictionary'),('nodi','no-dictionary')]


#class CourseForm(forms.Form):
#    lang_code=forms.CharField(widget=forms.Select(choices=LANG_CODES))

class CourseForm(djangoforms.ModelForm):
    lang_code=forms.CharField(widget=forms.Select(choices=LANG_CODES),label='Language')
    region_code=forms.CharField(widget=forms.Select(choices=REGIONS),label='Region')
    level_code=forms.CharField(widget=forms.Select(choices=LEVEL),label='Level')
    type_code=forms.CharField(widget=forms.Select(choices=COURSE_TYPE),label='Type')
    summary=forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows': 2}))
    class Meta:
        model=models.Course
        fields=('title','lang_code','region_code','level_code','type_code','summary')
        #exclude = ('content_blob','content','ready','content_count','rating','downtimes')
        
class ContentForm(djangoforms.ModelForm):
    class Meta:
        model=models.Course
        fields = ('content')
  
class EditContentForm(forms.Form):
    content=forms.CharField(required=True,widget=forms.Textarea(attrs={'rows':20, 'cols':40}))
    