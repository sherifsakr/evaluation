from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
import datetime
from django.forms import modelformset_factory
from .models import *
from django.forms import ModelForm, Textarea,TextInput,DateField
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelChoiceField
from django.core.exceptions import ValidationError


class TeamModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.empname
    
class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control has-feedback-left',
                                   'placeholder': _('User Name')}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control has-feedback-left',
                                   'placeholder':_('Password')}))



class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.fields['status'].empty_label = None
        self.fields['name'].widget.attrs['maxlength'] =255
        self.fields['delegationto'].empty_label = _("Select Employee")
     #fields   
    delegationto = TeamModelChoiceField(queryset=Employee.objects.all(),to_field_name="empid" ,
                     empty_label=_("Select Employee"),
                     widget=forms.Select(attrs={'class': 'chosen form-control col-md-3'} ),
                     label=_("Delegation To"),
                     required=False,help_text="ØªÙ�ÙˆÙŠØ¶ Ø¥Ø¯Ø§Ø±Ø© Ø§Ù„Ù…Ø´Ø±ÙˆØ¹ Ø§Ù„Ù‰ Ù…ÙˆØ¸Ù� Ø¢Ø®Ø±",
                     )

    class Meta:
        model = Project
        fields = ['name','start','status','end','desc','delegationto']

       # status = models.ForeignKey(ProjectStatus, widget=forms.Select({'class': 'form-control','placeholder':'task'}) )
        widgets = {
            'name':TextInput(attrs={'class': 'form-control','placeholder':_('Project Name'),'required': True}),
            'start':TextInput(attrs={'class': 'form-control has-feedback-left col-md-3 col-sm-9 col-xs-12 ','id':'single_cal_1','aria-describedby':'inputSuccess2Status','placeholder':_('Start Date'),'required': True}),
            'end':TextInput(attrs={'class': 'form-control has-feedback-left col-md-6 ','id':'single_cal_2','aria-describedby':'inputSuccess2Status','placeholder':_('End Date'),'required': True}),
            'desc': Textarea(attrs={'class':'form-control','placeholder':_('Project Details'),'required': True}),
            'status':forms.Select(attrs={'class': 'form-control','placeholder':_('Select Status')}),
        }
        labels = {
            'name': _('Project Name'),
            'status': _('Status'),
            'start':_('Start Date'),
            'end':_('End Date'),
            'desc':_('Project Description'),
        }
        help_texts = {
            'desc': _('write a Description for Project .'),
            'start':_('Please use the following format: <em>YYYY-MM-DD</em>.'),
            'end':_('Please use the following format: <em>YYYY-MM-DD</em>.'),
        }
        error_messages = {
            'name': {
                    'max_length': _("The Project's name is too long."),
                    'required': _("Project's name is required."),
             },
            'start': {
                    'required': _("Start Date  is required."),
             },
            'end': {
                    'required': _("End Date  is required."),
             },
            'desc': {
                    'max_length': _("The Project's Description is too long."),
                    'required': _("Description is required."),
             },

        }
    def clean(self):
        cleaned_data = super().clean()
        end = cleaned_data.get("end")
        start = cleaned_data.get("start")
        #Check end date less than start date
        if end < start:
            msg = _("End date is less than start date")
            self.add_error('end', msg)
            
class EmployeeList(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.empname

class DepartmentList(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.deptname

class AddTaskForm(ModelForm):
    CHOICES = (('1', _('Employee'),), ('2', _('Department'),))
    employee = EmployeeList(queryset=Employee.objects.all(),to_field_name="empid",empty_label=_("Select Employee"),required=False,widget=forms.Select(attrs={'class': 'chosen form-control','disabled':'disabled'} ))
    department_list = DepartmentList(queryset=Department.objects.all(),to_field_name="deptcode",empty_label=_("Select Departement"),required=False,widget=forms.Select(attrs={'class': 'chosen form-control','disabled':'disabled'} ))
    assigntype = forms.ChoiceField(label=_('Assignto'),required=False,widget=forms.RadioSelect(attrs={'class':'form-check-input-task'}), choices=CHOICES)

    class Meta:
        model = Task
        fields = ['name','desc','assigntype',
        'employee',
        'department_list','startdate','enddate']
        widgets = {
            'name':TextInput(attrs={'class': 'form-control','placeholder':_('Task Name'),'required': True}),
            'desc': Textarea(attrs={'id':'summernote','class':'form-control','placeholder':_('Task Details'),'required': True}),
            'startdate':TextInput(attrs={'class': 'form-control has-feedback-left col-md-3 col-sm-9 col-xs-12 ','id':'single_cal_1','aria-describedby':'inputSuccess2Status','placeholder':_('Start Date'),'required': True}),
            'enddate':TextInput(attrs={'class': 'form-control has-feedback-left col-md-6 ','id':'single_cal_2','aria-describedby':'inputSuccess2Status','placeholder':_('End Date'),'required': True}),
        }

        labels = {
            'name': _('Task Name'),
            'desc':_('Task Description'),
            'assigntype':_('Assignto'),
            'startdate':_('Start Date'),
            'enddate':_('End Date'),
        }
        help_texts = {
            'desc': _('write a Description for task .'),
            'startdate':_('Please use the following format: <em>YYYY-MM-DD</em>.'),
            'enddate':_('Please use the following format: <em>YYYY-MM-DD</em>.'),
        }
        error_messages = {
            'name': {
                    'max_length': _("The Project's name is too long."),
                    'required': _("Project's name is required."),
             },
            'startdate': {
                    'required': _("Start Date  is required."),
             },
            'enddate': {
                    'required': _("End Date  is required."),
             },
            'desc': {
                    'max_length': _("The Task's Description is too long."),
                    'required': _("Description is required."),
             },

        }
    def clean(self):
        cleaned_data = super().clean()
        enddate = cleaned_data.get("enddate")
        startdate = cleaned_data.get("startdate")
        #Check end date less than start date
        if enddate < startdate:
            msg = _("End date is less than start date")
            self.add_error('enddate', msg)

class EditTaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditTaskForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['maxlength'] =255

    CHOICES = (('1', _('Employee'),), ('2', _('Department'),))
    createdby = EmployeeList(queryset=Employee.objects.all(),to_field_name="empid", empty_label="(Nothing)",required=False,widget=forms.Select(attrs={'class': 'chosen form-control'} ))
    department_list = DepartmentList(queryset=Department.objects.all(),to_field_name="deptcode", empty_label=_("Select Departement"),required=False,widget=forms.Select(attrs={'class': 'chosen form-control','disabled':'disabled'} ))
    assigntype = forms.ChoiceField(label=_('Assignto'),required=False,widget=forms.RadioSelect(attrs={'class':'form-check-input-task'}), choices=CHOICES)
    note = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','label':_("Note"),'placeholder':_("Note"), 'rows':'3','size': '40','required': 'True'}),required=False, max_length=250, error_messages={'required': 'note'})
    progress = forms.IntegerField(validators=[ MaxValueValidator(100, message="Progress Over 100"),MinValueValidator(0, message="Progress less 0")],min_value=0, max_value=100)
    assigned_to=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':_('Responsible'),'required': False,}),required=False)
    class Meta:
        model = Task
        fields = ['name','desc','startdate','enddate','finisheddate','assigntype','status','progress']
        widgets = {
            'name':TextInput(attrs={'class': 'form-control','placeholder':_('Task Name'),'required': True}),
            'desc': Textarea(attrs={ 'id':'summernote','class':'form-control ','placeholder':_('Task Details'),'required': True}),
            'startdate':TextInput(attrs={'class': 'form-control has-feedback-left col-md-3 col-sm-9 col-xs-12 ','id':'single_cal_1','aria-describedby':'inputSuccess2Status','placeholder':_('Start Date'),'required': False}),
            'enddate':TextInput(attrs={'class': 'form-control has-feedback-left col-md-6 ','id':'single_cal_2','aria-describedby':'inputSuccess2Status','placeholder':_('End Date'),'required': False}),
            'finisheddate':TextInput(attrs={'class': 'form-control has-feedback-left col-md-6 ','id':'single_cal_3','aria-describedby':'inputSuccess2Status','placeholder':_('End Date'),'required': False}),
            'assignedto':TextInput(attrs={'class': 'form-control','placeholder':_('Responsible'),'required': False,}),
            'progress': forms.NumberInput(attrs={'class': 'form-control','placeholder':_('Progress'),'required': False,'min': 0, 'max': 100 }),
            'status':forms.Select(attrs={'class': 'form-control','placeholder':_('Select Status')})

        }
        labels = {
            'name': _('Task Name'),
            'desc':_('Task Description'),
            'assigntype':_('Assignto'),
        }
        error_messages = {
            'name': {
                    'max_length': _("The Task's name is too long."),
                    'required': _("Task's name is required."),
             },
            'startdate': {
                    'required': _("Start Date  is required."),
             },
            'enddate': {
                    'required': _("End Date  is required."),
             },
            'desc': {
                    'max_length': _("The Task's Description is too long."),
                    'required': _("Description is required."),
             },
            'progress': {
                    'MaxValueValidator': _("The Task's Pogress is over rang 100."),
                    'MinValueValidator': _("Task's name is less than 0."),
             },
            'status': {
                    'required': _("Status is required."),
             },

        }
    def clean(self):
        cleaned_data = super().clean()
        enddate = cleaned_data.get("enddate")
        startdate = cleaned_data.get("startdate")
        #Check end date less than start date
        if enddate < startdate:
            msg = _("End date is less than start date")
            self.add_error('enddate', msg)



class AuthorityForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = ['authority_notes',]
        labels = {
            'authority_notes': _('authority notes'),
        }
        widgets = {
            'authority_notes': Textarea(attrs={'class':'form-control','placeholder':_('strength point'),'rows':'3','required': False}),
           }

class EvaluationForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = ['strength_point','weaknesses',
                  'recommendations','director_notes',
                  'authority_notes','employeeid',
                  'q1', 'q2', 'q3', 'q4', 'q5','q6', 'q7', 'q8', 'q9', 'q10',
                  'q11', 'q12', 'q13', 'q14', 'q15','q16', 'q17',
                  'q18', 'q19', 'q20', 'q21', 'q22','q23', 'q24','q25',
                  'total_group1','total_group2','total_group3','total',
                  'is_excellent','is_vergood','is_good','is_fair','is_unacceptable',
                  ]
        labels = {
            'strength_point': _('strength point'),
            'weaknesses': _('weaknesses'),
            'recommendations': _('recommendations'),
            'director_notes': _('director notes'),
            'authority_notes': _('authority notes'),
            'employeeid': _('employeeid'),
        }
        widgets = {
            'strength_point': Textarea(attrs={'class':'form-control','placeholder':_('strength point'),'rows':'3','required': False}),
             'weaknesses': Textarea(attrs={'class':'form-control','placeholder':_('weaknesses'),'rows':'3','required': False}),
             'recommendations': Textarea(attrs={'class':'form-control','placeholder':_('recommendations'),'rows':'3','required': False}),
             'director_notes': Textarea(attrs={'class':'form-control','placeholder':_('director_notes'),'rows':'3','required': False}),
             'authority_notes': Textarea(attrs={'class':'form-control','placeholder':_('authority_notes'),'rows':'3','required': False}),
             'employeeid':forms.HiddenInput(),
             
            'q1': forms.NumberInput(attrs={'ng-model':'q1', 'class': 'form-control target','placeholder':_(''),'required': True }),
            'q2': forms.NumberInput(attrs={'ng-model':'q2', 'class': 'form-control target','placeholder':_(''),'required': True }),
            'q3': forms.NumberInput(attrs={'onchange':'','class': 'form-control target','placeholder':_(''),'required': True }),
            'q4': forms.NumberInput(attrs={'class': 'form-control target','placeholder':_(''),'required': True }),
            'q5': forms.NumberInput(attrs={'onchange':"this.value = minmax(this.value, 0, 6);loadData();", 'class': 'form-control target','placeholder':_(''),'required': True }),
            'q6': forms.NumberInput(attrs={'ng-model':'q6', 'class': 'form-control target','placeholder':_(''),'required': True }),
            'q7': forms.NumberInput(attrs={'ng-model':'q7', 'class': 'form-control target','placeholder':_(''),'required': True }),
            'q8': forms.NumberInput(attrs={'ng-model':'q8', 'class': 'form-control target','placeholder':_(''),'required': True }),
            'q9': forms.NumberInput(attrs={'ng-model':'q9', 'class': 'form-control target','placeholder':_(''),'required': True }),
            'q10': forms.NumberInput(attrs={'ng-model':'q10', 'class': 'form-control target','placeholder':_(''),'required': True }),
            'q11': forms.NumberInput(attrs={'ng-model':'q11', 'class': 'form-control target','placeholder':_(''),'required': True}),
            'q12': forms.NumberInput(attrs={'ng-model':'q12', 'class': 'form-control target','placeholder':_(''),'required': True,}),
            'q13': forms.NumberInput(attrs={'ng-model':'q13', 'class': 'form-control target','placeholder':_(''),'required': True }),
            'q14': forms.NumberInput(attrs={'ng-model':'q14', 'class': 'form-control target','placeholder':_(''),'required': True,}),
            'q15': forms.NumberInput(attrs={'ng-model':'q15', 'class': 'form-control target','placeholder':_(''),'required': True }),
            'q16': forms.NumberInput(attrs={'ng-model':'q16', 'class': 'form-control target','placeholder':_(''),'required': True }),
            'q17': forms.NumberInput(attrs={'ng-model':'q17', 'class': 'form-control target','placeholder':_(''),'required': True }),
            'q18': forms.NumberInput(attrs={'ng-model':'q18', 'class': 'form-control target','placeholder':_(''),'required': True }),
            'q19': forms.NumberInput(attrs={'ng-model':'q19', 'class': 'form-control target','placeholder':_(''),'required': True }),
            'q20': forms.NumberInput(attrs={'ng-model':'q20', 'class': 'form-control target','placeholder':_(''),'required': True }),
            'q21': forms.NumberInput(attrs={'ng-model':'q21', 'class': 'form-control target','placeholder':_(''),'required': True }),
            'q22': forms.NumberInput(attrs={'ng-model':'q22', 'class': 'form-control target','placeholder':_(''),'required': True }),
            'q23': forms.NumberInput(attrs={'ng-model':'q23', 'class': 'form-control target','placeholder':_(''),'required': True }),
            'q24': forms.NumberInput(attrs={'ng-model':'q24', 'class': 'form-control target','placeholder':_(''),'required': True }),
            'q25': forms.NumberInput(attrs={'ng-model':'q25', 'class': 'form-control target','placeholder':_(''),'required': True }),
            
            'total_group1': forms.NumberInput(attrs={'class': 'form-control ','placeholder':_('') }),

        }
