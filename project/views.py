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
          
        else:
            return login(request, *args, **kwargs)
    return login(request, *args, **kwargs)


@login_required
def EmployeeList(request):
    employees= EmployeeEv.objects.filter(Q(managercode__exact=request.session['EmpID']))
    context={'emps':employees,}
    return render(request, 'project/employee_list.html', context)
   

@login_required
def EvaluationPage(request,empid):
    #check if correct employee
    try:
        employee= EmployeeEv.objects.get(Q(managercode__exact=request.session['EmpID']) & Q(empid__exact=empid))
    except:
       raise Http404 
    
    if employee.job_grade is None :
          messages.info(request, _("لا يوجد درجة وظيفية  ! الرجاء تحديث البيانات"))
#         return HttpResponseRedirect(reverse('ns-project:employee-list'  ))
   #check if employee has evaluation in db
    try:
        evaluation = Evaluation.objects.get(Q(employeeid__exact = empid))
        if evaluation is not None :
            messages.success(request, _("تم عمل التقييم للموظف سابقا"))
            return HttpResponseRedirect(reverse('ns-project:employee-list'  ))
    except:
        pass
#     
#     try:
#        empView = ApIpCurrJobDataView.objects.get(Q(employee_id__exact = empid))
#     except:
#             messages.info(request, _("بيانات الموظف غير محدثة"))
#             return HttpResponseRedirect(reverse('ns-project:employee-list'  ))
  
    #profile data   
    emp = dict()
    emp= getEmpInfo(employee)
    
    #load form evaluation items
    empCategory= getEmpCat(employee)
    emp['cat']= empCategory['cat']
    evaluationItems = empCategory['evaluationItems'] 
    if  emp['cat']== None:
        messages.info(request, _("لا يوجد درجه وظيفية للموظف"))
        return HttpResponseRedirect(reverse('ns-project:employee-list'  ))
        
    if request.method == 'POST':
        #validat correct employee again
        employee= EmployeeEv.objects.get(Q(managercode__exact=request.session['EmpID']) & Q(empid__exact = request.POST['employeeid']))

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
            evObject.managerid = Employee.objects.get(empid__exact= employee.managercode) 
            authorityid= ManagerLevel.objects.filter(manager_id__exact = employee.managercode )[0]
            evObject.authorityid = Employee.objects.get(empid__exact= authorityid.manage_level2)   
            if 'save_only' in request.POST:
                evObject.status="Preparation"
            if 'save_send' in request.POST:
                evObject.status="InProgress"
            #count degree
            #group1
            evObject.total_group1 = 0
            for x in range(1, 18):
                q = str ("q" )+ str(x)
                v = request.POST.get(q, 0)
                evObject.total_group1 += int(v)
            #group2    
            evObject.total_group2 = 0
            for x in range(18, 23):
                q = str ("q" )+ str(x)
                v = request.POST.get(q, 0)
                evObject.total_group2 += int(v)
            #group3       
            evObject.total_group3 = 0
            for x in range(23, 26):
                q = str ("q" )+ str(x)
                v = request.POST.get(q, 0)
                evObject.total_group3 += int(v)
            #total 
            evObject.total = evObject.total_group1+evObject.total_group2+evObject.total_group3
            #grad
            if 90 <= evObject.total <= 100:  
                evObject.is_excellent = 1
            elif 80 <= evObject.total <= 90:  
                evObject.is_vergood = 1
            elif 70 <= evObject.total <= 79:  
                evObject.is_good = 1  
            elif 69 <= evObject.total <= 60:  
                evObject.is_fair = 1 
            elif  evObject.total < 60:  
                evObject.is_unacceptable = 1         
            
            evObject.save()
            evaInstant= Evaluation.objects.get(id__exact=evObject.id)
            employee.submission = evaInstant 
            employee.save()
            messages.success(request, _("تم إضافة التقييم بنجاح للموظف")+" "+emp['name'])
            return HttpResponseRedirect(reverse('ns-project:employee-list'))
    else :
        form = EvaluationForm()  
        form.fields["employeeid"].initial=empid
        form.fields["authority_notes"].disabled=True
         #add javascript validation
        checkvalidation(form, emp['cat'])
         
     
            
 

    context={'emp':emp,'evItems':evaluationItems,'form':form}
    return render(request, 'project/evaluation_form.html', context)
 

#remove it in production         


@login_required
def EvaluationEdit(request,empid):
     #check if corect employee
    try:
        employee= EmployeeEv.objects.get(Q(managercode__exact= request.session['EmpID']) & Q(empid__exact = empid))
    except:
       raise Http404 
   
   #check if employee has evaluation in db
    try:
        evaluation = Evaluation.objects.get(Q(employeeid__exact = empid))
       
    except:
          return HttpResponseRedirect(reverse('ns-project:employee-list'))

    #profile data   
    emp = dict()
    emp= getEmpInfo(employee)
    
    #load form evaluation items
    empCategory= getEmpCat(employee)
    emp['cat']= empCategory['cat']
    evaluationItems = empCategory['evaluationItems'] 
    if  emp['cat']== None:
        messages.info(request, _("لا يوجد درجه وظيفية للموظف"))
        return HttpResponseRedirect(reverse('ns-project:employee-list'  ))

    #load form
    form = EvaluationForm(request.POST or None, instance=evaluation)
    #add javascript validation
    checkvalidation(form, emp['cat'])
    #disable edit in authity field
    form.fields["authority_notes"].disabled=True
        
    if emp['cat'] == "a":
          form.fields["q16"].required = False
          form.fields["q17"].required = False
    elif emp['cat'] == "b":
          form.fields["q1"].required = False
          form.fields["q2"].required = False
    if form.is_valid():
        evObject= form.save(commit=False) 
        evObject.last_update_by =  request.session['EmpID']
        evObject.last_update_date = datetime.now()
        evObject.managerid = Employee.objects.get(empid__exact= employee.managercode) 
        authorityid= ManagerLevel.objects.filter(manager_id__exact = employee.managercode )[0].manage_level2
        evObject.authorityid = Employee.objects.get(empid__exact= authorityid)   
      
        if 'save_only' in request.POST:
            evObject.status="Preparation"
        if 'save_send' in request.POST:
            evObject.status="InProgress"
       
        #count degree
        #group1
        evObject.total_group1 = 0
        for x in range(1, 18):
            q = str ("q" )+ str(x)
            v = request.POST.get(q, 0)
            evObject.total_group1 += int(v)
        #group2    
        evObject.total_group2 = 0
        for x in range(18, 23):
            q = str ("q" )+ str(x)
            v = request.POST.get(q, 0)
            evObject.total_group2 += int(v)
        #group3       
        evObject.total_group3 = 0
        for x in range(23, 26):
            q = str ("q" )+ str(x)
            v = request.POST.get(q, 0)
            evObject.total_group3 += int(v)
        #total 
        evObject.total = evObject.total_group1+evObject.total_group2+evObject.total_group3
        #grad
        if 90 <= evObject.total <= 100:  
            evObject.is_excellent = 1
        elif 80 <= evObject.total <= 90:  
            evObject.is_vergood = 1
        elif 70 <= evObject.total <= 79:  
            evObject.is_good = 1  
        elif 69 <= evObject.total <= 60:  
            evObject.is_fair = 1 
        elif  evObject.total < 60:  
            evObject.is_unacceptable = 1         
        
        evObject.save()
        evaInstant= Evaluation.objects.get(id__exact=evObject.id)
        employee.submission = evaInstant 
        employee.save()
        messages.success(request, _("تم تعديل التقييم بنجاه للموظف")+" "+emp['name'])
        return HttpResponseRedirect(reverse('ns-project:employee-list'  ))
            
    context={'emp':emp,'evItems':evaluationItems,'form':form,'evaluation':evaluation}
    return render(request, 'project/evaluation_form.html', context)



@login_required
def ApprovalEdit(request,empid):

   #check if employee has evaluation in db
    try:
        evaluation = Evaluation.objects.get(Q(employeeid__exact = empid) & Q(authorityid__exact = request.session['EmpID']))
        employee = evaluation.employeeid
    except:
          return HttpResponseRedirect(reverse('ns-project:employee-list'  ))
    #profile data   
    emp = dict()
    emp= getEmpInfo(employee)
    
    #load form evaluation items
    empCategory= getEmpCat(employee)
    emp['cat']= empCategory['cat']
    evaluationItems = empCategory['evaluationItems'] 
    if  emp['cat']== None:
        messages.info(request, _("لا يوجد درجه وظيفية للموظف"))
        return HttpResponseRedirect(reverse('ns-project:employee-list'  ))

    
    #load form
    form = AuthorityForm(request.POST or None, instance=evaluation)
    #form.fields["employeeid"].readonly=False

        
    if form.is_valid() :
        evObject= form.save(commit=False) 
        evObject.last_update_by =  request.session['EmpID']
        evObject.last_update_date = datetime.now()

        if 'decline' in request.POST:
            evObject.status="Cancelled"
            messages.success(request, _("تم رفض التقييم للموظف")+" "+emp['name'])
        if 'approve' in request.POST:
            messages.success(request, _("تم إعتماد التقييم بنجاح للموظف")+" "+emp['name'])
            evObject.status="Done"
        evObject.save(update_fields=['authority_notes','status' ])
        return HttpResponseRedirect(reverse('ns-project:approval-requests'  ))
    else:
      evaluation = Evaluation.objects.get(Q(employeeid__exact = empid) & Q(authorityid__exact = request.session['EmpID']))

    context={'emp':emp,'evItems':evaluationItems,'form':form,'evaluation':evaluation}
    return render(request, 'project/approval_edit.html', context)


@login_required
def ApprovalRequests(request):
    submissions= Evaluation.objects.filter(Q(authorityid__exact=request.session['EmpID']) & ~Q(status__exact= "Preparation")).order_by('-status')
    context={'submissions':submissions,}
    return render(request, 'project/approval_requests.html', context)

@login_required    
def AllEmployee(request):

    form = FollowupForm(request.GET)
    dept = request.GET.get('departement')
    status = request.GET.get('status')


   
    if status and dept:
        employees = EmployeeEv.objects.filter(Q(submission__status__exact=status) & Q(deptcode__exact=dept))

    elif dept :
         employees = EmployeeEv.objects.filter(Q(deptcode__exact=dept) )
         
    elif status:
        employees = EmployeeEv.objects.filter(Q(submission__status__exact=status) )
    else:
        employees= EmployeeEv.objects.filter( )
        
  
    if employees is not None:
        employees=employees.order_by('-id')
    
    res=employees.count()
    paginator = Paginator(employees,20) 
    page = request.GET.get('page')
    try:
        _plist = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        _plist = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        _plist = paginator.page(paginator.num_pages)
        
    context={'emps':_plist,'form':form,'res':res}
    return render(request, 'project/employee_list_all.html', context)



@login_required  
def EvalutionView(request,empid):
    
    
    #check if employee has evaluation in db
    try:
        if  request.user.groups.filter(name="hr").exists() == True:
             evaluation = Evaluation.objects.get(Q(employeeid__exact = empid))
        else   :
             evaluation = Evaluation.objects.get(Q(employeeid__exact = empid) & Q(managerid__exact = request.session['EmpID']))
    
        employee = evaluation.employeeid
    except:
      raise Http404 
         
   
  #profile data   
    emp = dict()
    emp= getEmpInfo(employee)
    
    #load form evaluation items
    empCategory= getEmpCat(employee)
    emp['cat']= empCategory['cat']
    evaluationItems = empCategory['evaluationItems'] 
    if  emp['cat']== None:
        messages.info(request, _("لا يوجد درجه وظيفية للموظف"))
        return HttpResponseRedirect(reverse('ns-project:employee-list'))

    context={'emp':emp,'evItems':evaluationItems,'evaluation':evaluation}
    return render(request, 'project/evaluation_view.html', context)


def checkvalidation(form,itemCat):
    form.fields["q3"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 7);loadData();"
    form.fields["q5"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 6);loadData();"
    form.fields["q7"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 5);loadData();"
    form.fields["q8"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 4);loadData();"
    form.fields["q9"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 4);loadData();"
    form.fields["q14"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 3);loadData();"
    form.fields["q15"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 3);loadData();"
    form.fields["q19"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 4);loadData();"
    form.fields["q20"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 4);loadData();"
    form.fields["q21"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 4);loadData();" 
    form.fields["q23"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 3);loadData();"
    form.fields["q24"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 3);loadData();" 
    form.fields["q25"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 3);loadData();" 
    if itemCat == "b":
            form.fields["q4"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 6);loadData();"
            form.fields["q6"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 7);loadData();"
            form.fields["q10"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 3);loadData();"
            form.fields["q11"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 3);loadData();"
            form.fields["q12"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 3);loadData();"
            form.fields["q13"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 4);loadData();"
            form.fields["q16"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 7);loadData();"
            form.fields["q17"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 7);loadData();"
            form.fields["q18"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 4);loadData();"
            form.fields["q22"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 3);loadData();"  
    elif itemCat == "a":
            form.fields["q1"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 6);loadData();"
            form.fields["q2"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 6);loadData();"
            form.fields["q4"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 7);loadData();"
            form.fields["q6"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 6);loadData();"
            form.fields["q10"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 4);loadData();"
            form.fields["q11"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 4);loadData();"
            form.fields["q12"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 4);loadData();"
            form.fields["q13"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 3);loadData();"  
            form.fields["q18"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 3);loadData();"
            form.fields["q22"].widget.attrs['onchange'] = "this.value = minmax(this.value, 0, 4);loadData();"  
    
def getEmpCat(employee):
    result = dict()
    if int(employee.job_grade) >= 47 and int(employee.job_grade) <= 49 :
       result['evaluationItems']= EvaluationItem.objects.filter(Q(is_class_a__exact = 1)).order_by('id')
       result['cat']="a"
    elif int(employee.job_grade) <= 46 :
       result['evaluationItems']= EvaluationItem.objects.filter(is_class_b__exact = 1).order_by('id')
       result['cat']="b"
    else :
        result = None
    return   result

def getEmpInfo(employee):
    emp = dict()
    emp= {'name':employee.empname,
         'deptname':employee.deptname,
         'jobTitle':employee.jobtitle,
         'jobGrad':employee.job_grade,
         'jobNo':employee.job_no,
         'gvrmntStartDate':employee.gvrmnt_start_date,
         'orgStartDate':employee.org_start_date,'city':employee.descreption_1,'regon':employee.descreption}
    return emp
    
def gentella_html(request):
    context = {'LANG': request.LANGUAGE_CODE}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.
    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('project/' + load_template)
    return HttpResponse(template.render(context, request))

