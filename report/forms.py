from django.forms import ModelForm
import django.forms as fm
from report.models import Report

# Create the form class.
class ReportForm(ModelForm):
     class Meta:
         model = Report
         fields = ['name', 'email', 'category', 'problem', 'detail' ]
         widgets = {
            'name':fm.TextInput(attrs={'class': 'form-control', }),
            'email':fm.EmailInput(attrs={'class': 'form-control', }),
            'category':fm.Select(attrs={'class': 'form-control', }),
            'problem':fm.TextInput(attrs={'class': 'form-control', }),
            'detail': fm.Textarea(attrs={'class': 'form-control', 'place-holder':"Probelm details."}),
        }