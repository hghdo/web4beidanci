from django.conf.urls.defaults import *

urlpatterns = patterns('courses.views',
    (r'^$','index'),
    (r'^list.xml','list'),
    (r'^new$','new'),
    (r'^create$','create'),
    (r'^(\w+)/file$','course_file'),
    url(r'^(\d+)/$','show',name='course_path'),
    url(r'^(\d+)/update$','update',name='update_course_path'),
    url(r'^(\d+)/edit$','edit',name='edit_course_path'),
    url(r'^(\d+)/content$','content',name='edit_content_path'),
    url(r'^(\d+)/del$','destroy',name='delete_course_path'),
    # Example:
    # (r'^foo/', include('foo.urls')),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)


