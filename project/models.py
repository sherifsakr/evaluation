from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from simple_history.models import HistoricalRecords
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.encoding import  python_2_unicode_compatible

class Department(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    deptname = models.CharField(db_column='DeptName', max_length=200, blank=True, null=True, unique=True)  # Field name made lowercase.
    managerid = models.CharField(db_column='ManagerId', max_length=45, blank=True, null=True)  # Field name made lowercase.
    deptcode = models.IntegerField(db_column='DeptCode', unique=True, blank=True, null=True)  # Field name made lowercase.
    managername = models.CharField(db_column='ManagerName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'department'

@python_2_unicode_compatible
class Employee(models.Model):
    empid = models.IntegerField(db_column='EmpId', unique=True)  # Field name made lowercase.
    empname = models.CharField(db_column='EmpName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    deptcode = models.CharField(db_column='DeptCode', max_length=45, blank=True, null=True)  # Field name made lowercase.
    deptname = models.CharField(db_column='DeptName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    ismanager = models.IntegerField(db_column='IsManager', blank=True, null=True)  # Field name made lowercase.
    ext = models.CharField(db_column='Ext', max_length=45, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='Mobile', max_length=45, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    jobtitle = models.CharField(db_column='JobTitle', max_length=200, blank=True, null=True)  # Field name made lowercase.
    managercode = models.BigIntegerField(db_column='ManagerCode', blank=True, null=True)  # Field name made lowercase.
    sexcode = models.CharField(db_column='SexCode', max_length=6, blank=True, null=True)  # Field name made lowercase.
    iscontract = models.IntegerField(db_column='IsContract', blank=True, null=True)  # Field name made lowercase.
    submission = models.ForeignKey('Evaluation',db_column='submissionId',to_field='id',related_name='Employee_Evaluation_id',on_delete=models.SET_NULL, blank=True, null=True)
   # status= models.CharField(db_column='DeptCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    
    def __str__(self):
        return "List: {}".format(self.empname)
    
    class Meta:
        managed = True
        db_table = 'employee'



class EmployeeEv(models.Model):
    empid = models.IntegerField(db_column='EmpId', unique=True)  # Field name made lowercase.
    empname = models.CharField(db_column='EmpName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    deptcode = models.CharField(db_column='DeptCode', max_length=45, blank=True, null=True)  # Field name made lowercase.
    deptname = models.CharField(db_column='DeptName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    ismanager = models.IntegerField(db_column='IsManager', blank=True, null=True)  # Field name made lowercase.
    ext = models.CharField(db_column='Ext', max_length=45, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='Mobile', max_length=45, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    jobtitle = models.CharField(db_column='JobTitle', max_length=200, blank=True, null=True)  # Field name made lowercase.
    managercode = models.BigIntegerField(db_column='ManagerCode', blank=True, null=True)  # Field name made lowercase.
    sexcode = models.CharField(db_column='SexCode', max_length=6, blank=True, null=True)  # Field name made lowercase.
    iscontract = models.IntegerField(db_column='IsContract', blank=True, null=True)  # Field name made lowercase.
    submission = models.ForeignKey('Evaluation',db_column='submissionId',to_field='id',related_name='Employee_ev_Evaluation_id',on_delete=models.SET_NULL, blank=True, null=True)

    job_grade = models.CharField(db_column='JOB_GRADE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    job_no = models.IntegerField(db_column='JOB_NO', blank=True, null=True)  # Field name made lowercase.
    descreption = models.CharField(db_column='DESCREPTION', max_length=21, blank=True, null=True)  # Field name made lowercase.
    descreption_1 = models.CharField(db_column='DESCREPTION_1', max_length=15, blank=True, null=True)  # Field name made lowercase.
    gvrmnt_start_date = models.CharField(db_column='GVRMNT_START_DATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    end_date = models.CharField(db_column='END_DATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    eval_grade = models.CharField(db_column='EVAL_GRADE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    org_start_date = models.CharField(db_column='ORG_START_DATE', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employee_ev'
        

@python_2_unicode_compatible
class EvaluationItem(models.Model):
    evaluation_fom_id = models.IntegerField(blank=True, null=True)
    evaluation_group_id = models.CharField(max_length=45, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    max_degree_a = models.IntegerField(blank=True, null=True)
    max_degree_b = models.IntegerField(blank=True, null=True)
    is_class_a = models.IntegerField(blank=True, null=True)
    is_class_b = models.IntegerField()
    degree = models.IntegerField()
    field_col = models.CharField(max_length=10,blank=True, null=True)
    
    def __str__(self):
        return "List: {}".format(self.title)
    
    class Meta:
        managed = True
        db_table = 'evaluation_item'
        


class Evaluation(models.Model):
    STATUS = (
        ('', _('Choice action')),
        ('New', _('جديد')),
        ('Preparation', _('تحت الإعداد')),
        ('InProgress', _('تحت الإعتماد')),
        ('Done', _('معتمد')),
        ('Cancelled', _('إعادة التقييم'))
    )
     
    status = models.CharField(db_column='Status',max_length=10,choices=STATUS, blank=False, null=False)  
    
    strength_point = models.CharField(max_length=300, blank=True, null=True)
    weaknesses = models.CharField(max_length=400, blank=True, null=True)
    recommendations = models.CharField(max_length=400, blank=True, null=True)
    director_notes = models.CharField(max_length=400, blank=True, null=True)
    authority_notes = models.CharField(max_length=400, blank=True, null=True)
    employeeid = models.ForeignKey('EmployeeEv',db_column='employeeid',to_field='empid',related_name='EmployeeEv_Evaluation_employeeid',on_delete=models.SET_NULL, blank=True, null=True)    
    managerid = models.ForeignKey('Employee',db_column='managerId',to_field='empid',related_name='Employee_Evaluation_managerid',on_delete=models.SET_NULL, blank=True, null=True)     
    authorityid =models.ForeignKey('Employee',db_column='authorityId',to_field='empid',related_name='Employee_Evaluation_authorityId',on_delete=models.SET_NULL, blank=True, null=True)      
    submit_by = models.IntegerField()
    submit_date = models.DateTimeField()
    last_update_by = models.IntegerField(blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    q1 = models.IntegerField(blank=True, null=True)
    q2 = models.IntegerField(blank=True, null=True)
    q3 = models.IntegerField()
    q4 = models.IntegerField()
    q5 = models.IntegerField()
    q6 = models.IntegerField()
    q7 = models.IntegerField()
    q8 = models.IntegerField()
    q9 = models.IntegerField()
    q10 = models.IntegerField()
    q11 = models.IntegerField()
    q12 = models.IntegerField()
    q13 = models.IntegerField()
    q14 = models.IntegerField()
    q15 = models.IntegerField()
    q16 = models.IntegerField()
    q17 = models.IntegerField()
    q18 = models.IntegerField()
    q19 = models.IntegerField()
    q20 = models.IntegerField()
    q21 = models.IntegerField()
    q22 = models.IntegerField()
    q23 = models.IntegerField()
    q24 = models.IntegerField()
    q25 = models.IntegerField()
    total_group1 = models.IntegerField(blank=True, null=True)
    total_group2 = models.IntegerField(blank=True, null=True)
    total_group3 = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    is_excellent = models.IntegerField(blank=True, null=True)
    is_vergood = models.IntegerField(blank=True, null=True)
    is_good = models.IntegerField(blank=True, null=True)
    is_fair = models.IntegerField(blank=True, null=True)
    is_unacceptable = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return "List: {}".format(self.evaluation_fom_id)
    
    class Meta:
        managed = False
        db_table = 'evaluation'


class ManagerLevel(models.Model):
    empid =models.IntegerField(blank=True, null=True)
    manager_id = models.IntegerField(blank=True, null=True)
    manage_level2 = models.IntegerField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'manager_level'
        

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'
           
class ApIpCurrJobDataView(models.Model):
    empindex = models.AutoField(db_column='empIndex', primary_key=True)  # Field name made lowercase.
    employee_id = models.BigIntegerField(db_column='EMPLOYEE_ID', unique=True, blank=True, null=True)  # Field name made lowercase.
    emp_name = models.CharField(db_column='EMP_NAME', max_length=42, blank=True, null=True)  # Field name made lowercase.
    gvrmnt_start_date = models.CharField(db_column='GVRMNT_START_DATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    org_start_date = models.CharField(db_column='ORG_START_DATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    office_phone = models.CharField(db_column='OFFICE_PHONE', max_length=7, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='MOBILE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    qual_code = models.IntegerField(db_column='QUAL_CODE', blank=True, null=True)  # Field name made lowercase.
    qual_desc = models.CharField(db_column='QUAL_DESC', max_length=50, blank=True, null=True)  # Field name made lowercase.
    qual_type = models.CharField(db_column='QUAL_TYPE', max_length=7, blank=True, null=True)  # Field name made lowercase.
    qual_type_desc = models.CharField(db_column='QUAL_TYPE_DESC', max_length=17, blank=True, null=True)  # Field name made lowercase.
    action_code = models.IntegerField(db_column='ACTION_CODE', blank=True, null=True)  # Field name made lowercase.
    job_grade = models.CharField(db_column='JOB_GRADE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    job_no = models.IntegerField(db_column='JOB_NO', blank=True, null=True)  # Field name made lowercase.
    job_title = models.CharField(db_column='JOB_TITLE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    job_step = models.CharField(db_column='JOB_STEP', max_length=2, blank=True, null=True)  # Field name made lowercase.
    action_start_date = models.CharField(db_column='ACTION_START_DATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    action_text = models.CharField(db_column='ACTION_TEXT', max_length=26, blank=True, null=True)  # Field name made lowercase.
    action_no = models.IntegerField(db_column='ACTION_NO', blank=True, null=True)  # Field name made lowercase.
    action_date = models.CharField(db_column='ACTION_DATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    action_end_date = models.CharField(db_column='ACTION_END_DATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    basic_salary = models.IntegerField(db_column='BASIC_SALARY', blank=True, null=True)  # Field name made lowercase.
    transportation = models.IntegerField(db_column='TRANSPORTATION', blank=True, null=True)  # Field name made lowercase.
    grade_basic_salary = models.CharField(db_column='GRADE_BASIC_SALARY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    grade_sort_no = models.CharField(db_column='GRADE_SORT_NO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    category_code = models.IntegerField(db_column='CATEGORY_CODE', blank=True, null=True)  # Field name made lowercase.
    cat_descreption = models.CharField(db_column='CAT_DESCREPTION', max_length=19, blank=True, null=True)  # Field name made lowercase.
    sex_code = models.IntegerField(db_column='SEX_CODE', blank=True, null=True)  # Field name made lowercase.
    birth_date = models.CharField(db_column='BIRTH_DATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    birth_place = models.CharField(db_column='BIRTH_PLACE', max_length=22, blank=True, null=True)  # Field name made lowercase.
    nationality = models.IntegerField(db_column='NATIONALITY', blank=True, null=True)  # Field name made lowercase.
    nat_descreption = models.CharField(db_column='NAT_DESCREPTION', max_length=20, blank=True, null=True)  # Field name made lowercase.
    current_dept_code = models.IntegerField(db_column='CURRENT_DEPT_CODE', blank=True, null=True)  # Field name made lowercase.
    dept_name = models.CharField(db_column='DEPT_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    working_dept_code = models.CharField(db_column='WORKING_DEPT_CODE', max_length=4, blank=True, null=True)  # Field name made lowercase.
    manager_id = models.CharField(db_column='MANAGER_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    authority_id = models.CharField(db_column='AUTHORITY_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    work_dept_name = models.CharField(db_column='WORK_DEPT_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    emp_type = models.IntegerField(db_column='EMP_TYPE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ap_ip_curr_job_data_view'
