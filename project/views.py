from django.shortcuts import render, render_to_response ,get_object_or_404,redirect
from django.template import loader
from django.http import HttpResponse ,HttpResponseRedirect,Http404 ,HttpResponseForbidden
from .models import *
from .forms import *
from evaluation.ldap import *
# from django.contrib.auth import login
from django.contrib.auth.views import *
from django.utils.translation import ugettext as _
from django.forms import formset_factory
from django.forms import BaseModelFormSet
from datetime import datetime , timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q , Count ,Avg
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import permission_required
from django.views.generic import UpdateView, ListView
# from .filters import SheetFilter
from django.template.loader import  render_to_string
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.core.urlresolvers import resolve
from simple_history.utils import update_change_reason
from idlelib.debugobj import _object_browser
from django.forms.models import modelformset_factory
from unittest.case import expectedFailure
from django.template.context_processors import request
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail, EmailMessage


def loginfromdrupal(request, email,signature,time):
    from django.contrib.auth import login
    import getpass
    import datetime
    """ Email function """
    def decrypted(text):
        from Crypto.Cipher import AES
        from Crypto.Cipher import DES
        import base64
        AES.key_size=128
        key = "5E712B225B5148E9"
        iv = "55FE52A86C3ABWED"
        crypt_object = AES.new(key=key,mode=AES.MODE_CBC,IV=iv)
        original = text
        plain = original.replace('-', "/")
        decoded=base64.b64decode(plain) # your ecrypted and encoded text goes here
        decrypted=crypt_object.decrypt(decoded)
        decrypted = decrypted.decode("utf-8")
        return decrypted
    """" return mail"""
    mail =decrypted(email)
    """ return ip """
    ip = 1
    ip = decrypted(signature)
    """ return time """
    time = decrypted(time)

    now = datetime.datetime.now()
    now_plus_10 = now + datetime.timedelta(minutes = 1)
    time_now = now.strftime('%H:%M')
    date_after_minute = now_plus_10.strftime('%H:%M')

    """ Current ip """
    current_ip = request.META.get('REMOTE_ADDR')
    """" Get url from"""
    URL = request.META.get('HTTP_REFERER')
    referer = None
    if URL:
        referer= URL.split("/")[-3]
    if referer == 'portal.stats.gov.sa':
        if ip == "192..168.2.84":
            if time == time_now or time == date_after_minute:
                username = mail
                try:
                    user = User.objects.get(username=username)
                    #manually set the backend attribute
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                except User.DoesNotExist:
                    from django_auth_ldap.backend import LDAPBackend
                    ldap_backend = LDAPBackend()
                    ldap_backend.populate_user(username)
                    # return HttpResponseRedirect(reverse('login'))
                try:
                    user = User.objects.get(username=username)
                    #manually set the backend attribute
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                except User.DoesNotExist:
                    return HttpResponseRedirect(reverse('login'))
                if request.user.is_authenticated():
                    email = request.user.email
                    emp = Employee.objects.filter(email= email)
                # Get all data filtered by user email and set in session
                    for data in emp:
                        request.session['EmpID'] = data.empid
                        request.session['EmpName'] = data.empname
                        request.session['DeptName'] = data.deptname
                        request.session['Mobile'] = data.mobile
                        request.session['DeptCode'] = data.deptcode
                        request.session['JobTitle'] = data.jobtitle
                        request.session['IsManager'] = data.ismanager
                    if emp:
                        if data.ismanager == 1:
                            g = Group.objects.get(name='ismanager')
                            g.user_set.add(request.user.id)
                        else:
                            g = Group.objects.get(name='employee')
                            g.user_set.add(request.user.id)
                else:
                    return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseRedirect(reverse('login'))

    logged = request.COOKIES.get('logged_in_status')
    context = {'logged':logged, "mail":mail,"ip":ip,"time1":time,"URL":referer}
    template = loader.get_template('project/index.html')
    return HttpResponseRedirect(reverse('ns-project:index'))

def myuser(request, *args, **kwargs):
    if request.method == "POST":
        form = BootstrapAuthenticationForm(request, data=request.POST)
        emp = None
        if form.is_valid():
          auth_login(request, form.get_user())
            # email = None 
        if request.user.is_authenticated():
            email = request.user.email
            try:
                emp = Employee.objects.filter(email__exact= email).get()
            except:
                #return HttpResponseRedirect(reverse('logout'))
                return HttpResponseRedirect(reverse('ns-project:login'))
  
        # Get all data filtered by user email and set in session
            if emp is not None:
                request.session['EmpID'] = emp.empid
                request.session['Email'] = emp.email
                request.session['EmpName'] = emp.empname
                request.session['DeptName'] = emp.deptname
                request.session['Mobile'] = emp.mobile
                request.session['DeptCode'] = emp.deptcode
                request.session['JobTitle'] = emp.jobtitle
                request.session['IsManager'] = emp.ismanager
                
                if emp.ismanager == 1:
                        g = Group.objects.get(name='ismanager')
                        g.user_set.add(request.user.id)
                else:
                        g = Group.objects.get(name='employee')
                        g.user_set.add(request.user.id)
                #check if user has delegation in some project and he has not any group at let give him projectdelegation
                if Project.objects.filter(delegationto__exact=emp.id).count() > 0 :
                    if request.user.groups.filter(name="ismanager"). exists() == False and request.user.groups.filter(name="projectmanager"). exists() == False:
                        g = Group.objects.get(name='projectdelegation')
                        g.user_set.add(request.user.id)
          
        else:
            return login(request, *args, **kwargs)
    return login(request, *args, **kwargs)

@login_required
def index(request):
    # Populate User From Ldap Without Login
    from django_auth_ldap.backend import LDAPBackend
    # ldap_backend = LDAPBackend()
    # ldap_backend.populate_user('aalbatil@stats.gov.sa')
    logged = request.COOKIES.get('logged_in_status')
    context = {'logged':logged}
    template = loader.get_template('project/index.html')
    return HttpResponse(template.render(context, request))

@login_required
def EmployeeList(request):
    employees= Employee.objects.filter(Q(managercode__exact=request.session['EmpID']))
    context={'emps':employees,}
    return render(request, 'project/employee_list.html', context)
   

@login_required
def EvaluationPage(request,empid):
    employee= Employee.objects.get(Q(managercode__exact=request.session['EmpID']) & Q(empid__exact=empid))
    try:
       empView = ApIpCurrJobDataView.objects.get(Q(employee_id__exact=empid))
    except:
       empView = None
    emp=dict()
    emp= {'name':employee.empname,
         'deptname':employee.deptname,
         'jobTitle':employee.jobtitle,
         'jobGrad':empView.job_grade,
         'jobNo':empView.job_no,
         'gvrmntStartDate':empView.gvrmnt_start_date,
         'orgStartDate':empView.org_start_date,}
    
    #load form evaluation items
    if int(empView.job_grade) >= 47 and int(empView.job_grade) <= 49 :
        evaluationItems= EvaluationItem.objects.filter(Q(is_class_a__exact = 1)).order_by('id')
        emp['cat']="a"
    elif int(empView.job_grade) <= 46 :
        evaluationItems= EvaluationItem.objects.filter(is_class_b__exact = 1).order_by('id')
        emp['cat']="b"
        
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if emp['cat'] == "a":
              form.fields["q16"].required = False
              form.fields["q17"].required = False
        elif emp['cat'] == "b":
              form.fields["q1"].required = False
              form.fields["q2"].required = False
        if form.is_valid():
            evObject= form.save(commit=False) 
            evObject.submit_by = request.session['EmpID']
            evObject.submit_date = datetime.now()
            evObject.save()
            
            messages.success(request, _("evaluation has been saved successfully for")+" "+emp['name'])
            return HttpResponseRedirect(reverse('ns-project:employee-list'  ))
    else :
         form = EvaluationForm()  
         form.fields["employeeid"].initial=empid
        
        
    
    context={'emp':emp,'evItems':evaluationItems,'form':form}
    return render(request, 'project/evaluation_form.html', context)
 

#remove it in production         
def gentella_html(request):
    context = {'LANG': request.LANGUAGE_CODE}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.
    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('project/' + load_template)
    return HttpResponse(template.render(context, request))

