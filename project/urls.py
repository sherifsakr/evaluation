from django.conf.urls import url ,include
from project import views
# from .api import  EmployeeViewSet, EvaluationViewSet
#from rest_framework import routers
#application namespace
app_name = 'ns-project'

# Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'employees_WebService', EmployeeViewSet)
# router.register(r'evaluations_webservice', EvaluationViewSet)

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.

    
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', views.EmployeeList, name='employee-list'),
    url(r'^employee_list/$', views.EmployeeList, name='employee_list'),
    url(r'^evaluation_form/(?P<empid>\d+)$', views.EvaluationPage, name='evaluation-form'),
    url(r'^evaluation-edit/(?P<empid>\d+)$', views.EvaluationEdit, name='evaluation-edit'),
    url(r'^approval_requests/$', views.ApprovalRequests, name='approval-requests'),
    url(r'^edit_approval/(?P<empid>\d+)$', views.ApprovalEdit, name='edit-approval'),
    url(r'^all_employee/$', views.AllEmployee, name='all-employee'),
    url(r'^evalution_view/(?P<empid>\d+)$', views.EvalutionView, name='evalution-view'),

    #login from drupal
    url(r'^auth/(?P<email>.*)/(?P<signature>.*)/(?P<time>.*)/$', views.loginfromdrupal, name='loginfromdrupal'),
    #main temp
    url(r'^.*\.html', views.gentella_html, name='gentella'),
    #url(r'^', include(router.urls)),
]
