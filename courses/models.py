from appengine_django.models import BaseModel
from google.appengine.ext import db
import courses
import logging

class Course(BaseModel):
    title           = db.StringProperty()
    summary         = db.TextProperty()
    lang_code       = db.StringProperty()
    region_code     = db.StringProperty()
    level_code      = db.StringProperty()
    type_code       = db.StringProperty()
    rating          = db.IntegerProperty()
    ready           = db.BooleanProperty()
    creator         = db.UserProperty()
    content         = db.TextProperty()
    content_count   = db.IntegerProperty()
    content_blob    = db.BlobProperty()
    
    def language(self):
        lang_dict=dict(courses.forms.LANG_CODES)
        logging.info(lang_dict)
        return lang_dict[self.lang_code]
    def region(self):
        region_dict=dict(courses.forms.REGIONS)
        return region_dict[self.region_code]
