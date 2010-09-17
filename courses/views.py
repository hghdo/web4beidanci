from xml.dom.minidom import getDOMImplementation
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core import serializers
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from courses.models import Course
from forms import *
from appengine_django.auth.decorators import login_required
import datetime
import logging
from struct import *
from google.appengine.ext import db
from google.appengine.ext.db import Key
from google.appengine.api import users
from google.appengine.ext.db import GqlQuery
import md5


def index(request):
    user = users.get_current_user()
    admin = users.is_current_user_admin()
#    query = db.GqlQuery("SELECT * FROM Course WHERE content_count > :1 OR creator = :2 ",
#                    10, users.get_current_user())
    style = request.GET.get('style') or 'pop'
    #logging('request style is=>'+style)
    if style=='pop':
        query = GqlQuery("SELECT * FROM Course WHERE ready = :1 ORDER BY rating",True)
        #q=Course.objects.all().filter("content_count >",10).order('rating')
    elif style=='rec':
        query = GqlQuery("SELECT * FROM Course WHERE ready = :1 ORDER BY created_at DESC",True)
        #q=Course.objects.all().filter("content_count >",10).order('-created_at')
    elif style=='self':
        query = Course.all().filter("creator =",users.get_current_user())
    elif style=='admin' and admin:
        query = Course.all()
    else:
        query = GqlQuery("SELECT * FROM Course WHERE ready = :1 ORDER BY rating",True)
        style="pop"
    return render_to_response('courses/index.html',{'courses':query.fetch(10),'style':style,'user':user,'admin':admin})

def list(request):
    impl = getDOMImplementation()
    doc=impl.createDocument(None, "course-list", None)
    q=Course.objects.all()
    q.filter("content_count >",10)
    list=q.fetch(10)
    for course in list:
        course.xml(doc,path_prefix=request.get_host())
    #data=serializers.serialize("xml",Course.objects.all(),fields=('title','summary'))
    data=doc.toxml('utf-8')
    return HttpResponse(data, mimetype="text/xml")

def course_file(request,course_key):
    key=Key(encoded=course_key)
    course=Course.get(key)
    course.downtimes=course.downtimes+1
    course.put()
    response = HttpResponse(mimetype='text')
    response['Content-Disposition'] = 'attachment; filename='+course_key+'.cou'
    response.write(course.content_blob)
    return response
    

def show(request,course_id):
    cid=int(course_id)
    course=Course.get_by_id(cid)
    editable=(course==users.get_current_user() or users.is_current_user_admin())
    return render_to_response('courses/show.html',{'course':course,'editable':editable})
    
@login_required    
def edit(request,course_id):
    cid=int(course_id)
    course=Course.get_by_id(cid)
    course_form=CourseForm(instance=course)
    return render_to_response('courses/edit.html',{'form':course_form,'course':course,'user':users.get_current_user()})

@login_required    
def update(request,course_id):
    cid=int(course_id)
    course=Course.get_by_id(cid)
    course_form=CourseForm(request.POST,instance=course)
    if course_form.is_valid():
        course=course_form.save()
        return HttpResponseRedirect(reverse('course_path',args=[cid]))
    else:
        return render_to_response('courses/edit.html',{'form':course_form,'user':users.get_current_user()})
    
@login_required
def new(request):
    course_form=CourseForm()
    return render_to_response('courses/new.html',{'form':course_form,'user':users.get_current_user()})

@login_required    
def create(request):
    course_form=CourseForm(request.POST)
    if course_form.is_valid():
        course=course_form.save()
        return HttpResponseRedirect(reverse('course_path',args=[course.key().id()]))
    else:
        return render_to_response('courses/new.html',{'form':course_form,'user':users.get_current_user()})
    
@login_required    
def destroy(request,course_id):
    cid=int(course_id)
    course=Course.get_by_id(cid)
    if course.creator==users.get_current_user() or users.is_current_user_admin():
        db.delete(course)
    return HttpResponseRedirect(reverse('courses.views.index'))



@login_required    
def content(request,course_id):
    cid=int(course_id)
    course=Course.get_by_id(cid)
    if request.method == 'GET':
        form=EditContentForm({'content':course.content})
        return render_to_response('courses/content.html',{'form':form,'course':course,'path':request.path,'user':users.get_current_user()})
    elif request.method == 'POST':
        form=EditContentForm(request.POST)
        if form.is_valid():
            text_content=form.cleaned_data['content']
            #text_content=text_content.encode('utf-8')
            bb=text_content.replace('\r\n','$')
            text_content=bb.replace('$','\n')
            course.content=text_content
            lines=text_content.strip().splitlines()
            course.content_count=len(lines)
            # create course header
            course_header="title:%s\n" % course.title
            course_header+="language:%s\n" % course.lang_code
            course_header+="region:%s\n" % course.region_code
            course_header+="level:%s\n" % 'fundamental'
            #course_header+="version:#{gen_course_file_at.to_i}\n"
            course_header+="type:%s\n" % 'simple'
            course_header+="content_count:%s\n" % len(lines)
            course_header+="separator:10\n"
            header_size_binary_str=pack('!h',len(course_header.encode('utf-8')))
            content_str=header_size_binary_str+course_header.encode('utf-8')+text_content.encode('utf-8')
            course.content_blob=db.Blob(content_str)
            new_md5=md5.new(content_str).hexdigest()
            if len(lines)>10:
                course.ready=True
            #logging.info(course.content)
            if new_md5!=course.md5_digest:
                course.md5_digest=new_md5
                course.put()
            return HttpResponseRedirect(reverse('course_path',args=[cid]))