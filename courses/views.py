from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from courses.models import Course
from forms import *
from appengine_django.auth.decorators import login_required
import datetime
import logging
from struct import *
from google.appengine.ext import db


def index(request):
    return render_to_response('courses/index.html',{'courses':Course.objects.all()})

def show(request,course_id):
    cid=int(course_id)
    course=Course.get_by_id(cid)
    return render_to_response('courses/show.html',{'course':course})
    
@login_required
def new(request):
    course_form=CourseForm()
    return render_to_response('courses/new.html',{'form':course_form})
    
def create(request):
    course_form=CourseForm(request.POST)
    if course_form.is_valid():
        course=course_form.save()
        return HttpResponseRedirect(reverse('courses.views.index'))
    else:
        return render_to_response('courses/new.html',{'form':course_form})
    
def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html',{'current_date':now})


def content(request,course_id):
    cid=int(course_id)
    course=Course.get_by_id(cid)
    if request.method == 'GET':
        form=EditContentForm({'content':course.content})
        return render_to_response('courses/content.html',{'form':form,'path':request.path})
    elif request.method == 'POST':
        form=EditContentForm(request.POST)
        if form.is_valid():
            text_content=form.cleaned_data['content']
            lines=text_content.strip().splitlines()
            # create course header
            course_header="title:%s\n" % course.title
            course_header+="language:%s\n" % course.lang_code
            course_header+="region:%s\n" % course.region_code
            course_header+="level:%s\n" % 'fundamental'
            #course_header+="version:#{gen_course_file_at.to_i}\n"
            course_header+="type:%s\n" % 'simple'
            course_header+="content_count:%s\n" % len(lines)
            course_header+="separator:10\n"
            header_size_binary_str=pack('!h',len(course_header))
            content_str=header_size_binary_str+course_header+text_content  
            course.content=text_content
            course.content_blob=db.Blob(content_str.encode('utf-8'))
            course.content_count=len(lines)
            logging.info(course.content)
            course.put()
            return HttpResponseRedirect(reverse('edit_content_path',args=[cid]))
        