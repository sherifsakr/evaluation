from django.conf.urls import url ,include
from project import views

#application namespace
app_name = 'ns-project'

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.


    # The home page

    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', views.EmployeeList, name='employee-list'),
    url(r'^employee_list/$', views.EmployeeList, name='employee_list'),
    url(r'^evaluation_form/(?P<empid>\d+)$', views.EvaluationForm, name='evaluation-form'),
 
    #login from drupal
    url(r'^auth/(?P<email>.*)/(?P<signature>.*)/(?P<time>.*)/$', views.loginfromdrupal, name='loginfromdrupal'),
    #main temp
    url(r'^.*\.html', views.gentella_html, name='gentella'),
   
]
