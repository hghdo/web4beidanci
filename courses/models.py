from appengine_django.models import BaseModel
from google.appengine.ext import db
import courses
import logging

class Course(BaseModel):
    title           = db.StringProperty(required=True)
    summary         = db.TextProperty(default='')
    lang_code       = db.StringProperty(required=True)
    region_code     = db.StringProperty(required=True)
    level_code      = db.StringProperty(required=True)
    type_code       = db.StringProperty(required=True)
    rating          = db.RatingProperty(default=1)
    downtimes       = db.IntegerProperty(default=0)
    ready           = db.BooleanProperty()
    creator         = db.UserProperty(auto_current_user_add=True,required=True)
    created_at      = db.DateTimeProperty(auto_now_add=True,required=True)
    updated_at      = db.DateTimeProperty()
    md5_digest      = db.StringProperty()
    ready           = db.BooleanProperty(default=False)
    content         = db.TextProperty()
    content_count   = db.IntegerProperty(default=0)
    content_blob    = db.BlobProperty()
    
    def language(self):
        lang_dict=dict(courses.forms.LANG_CODES)
        logging.info(lang_dict)
        return lang_dict[self.lang_code]
    def region(self):
        region_dict=dict(courses.forms.REGIONS)
        return region_dict[self.region_code]
    
    def xml(self,doc,path_prefix="172.29.1.67:8000"):
        top_element = doc.documentElement
        c_tag=doc.createElement('course')       
        tag = doc.createElement('key')
        text = doc.createTextNode(str(self.key()))
        tag.appendChild(text)
        c_tag.appendChild(tag)
        tag = doc.createElement('title')
        text = doc.createTextNode(self.title)
        tag.appendChild(text)
        c_tag.appendChild(tag)
        tag = doc.createElement('summary')
        text = doc.createTextNode(self.summary)
        tag.appendChild(text)
        c_tag.appendChild(tag)
        tag = doc.createElement('language')
        text = doc.createTextNode(self.language())
        tag.appendChild(text)
        c_tag.appendChild(tag)
        tag = doc.createElement('content_count')
        text = doc.createTextNode(str(self.content_count))
        tag.appendChild(text)
        c_tag.appendChild(tag)
        tag = doc.createElement('url')
        text = doc.createTextNode('http://'+path_prefix+'/courses/'+str(self.key())+'/file')
        tag.appendChild(text)
        c_tag.appendChild(tag)
        tag = doc.createElement('filename')
        text = doc.createTextNode(str(self.key())+'.cou')
        tag.appendChild(text)
        c_tag.appendChild(tag)
        tag = doc.createElement('md5')
        text = doc.createTextNode(self.md5_digest)
        tag.appendChild(text)
        c_tag.appendChild(tag)

        top_element.appendChild(c_tag)
