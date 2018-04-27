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



     
class EmployeeList(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.empname

class DepartmentList(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.deptname




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
        
class TeamModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.empname   
 
class FollowupModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.deptname
            
class FollowupForm(forms.Form):
   
      departement = FollowupModelChoiceField(queryset=Department.objects.filter().all(), to_field_name="deptcode",empty_label=_('Select Departement'),widget=forms.Select(attrs={'class': 'chosen chosen form-control col-md-3'} ),required=False,error_messages={'required': _('Please Sealect Departement')},label=_('Departement'))
      employee = TeamModelChoiceField(queryset=Employee.objects.all(),to_field_name="empid" ,empty_label=_("Select Employee"),widget=forms.Select(attrs={'class': 'chosen form-control col-md-3'} ),required=False,label=_('Employee'))
      STATUS = (
        ('', _('Choice action')),
        ('Preparation', _('تحت الإعداد')),
        ('InProgress', _('تحت الإعتماد')),
        ('Done', _('معتمد')),
        ('Cancelled', _('إعادة التقييم'))
        )
      status= forms.ChoiceField(choices=STATUS,required=False,label=_("Status"),widget=forms.Select(attrs={'class': ' form-control col-md-3 chosen'}) )

