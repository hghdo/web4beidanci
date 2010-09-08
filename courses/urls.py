from django.conf.urls.defaults import *

urlpatterns = patterns('courses.views',
    (r'^$','index'),
    (r'^new$','new'),
    (r'^create$','create'),
    url(r'^(\d+)/content$','content',name='edit_content_path'),
    url(r'^(\d+)/$','show',name='course_path'),
    # Example:
    # (r'^foo/', include('foo.urls')),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)


