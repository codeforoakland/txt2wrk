from django import forms
from django.contrib.auth import authenticate
from common.helpers import USPhoneNumberField
from django.utils.translation import ugettext_lazy as _

from applicant.models import ApplicantProfile
from job.models import Job
from models import Call

class ReceiveCallForm(forms.Form):
    
    From = USPhoneNumberField(required=True)
    CallSid = forms.CharField(required=True)

class HandleFragmentForm(forms.Form):
    
    CallSid = forms.CharField(required=True)
    Digits = forms.CharField(required=False)
    
class VerifyPasswordForm(forms.Form):
    
    CallSid = forms.CharField(required=True)
    Digits = forms.CharField(required=True)
    
    def clean(self):
        if 'Digits' in self.cleaned_data:
            call = Call.objects.get(call_sid=self.cleaned_data['CallSid'])
            profile = call.applicant
            user = authenticate(username=profile.mobile_number, password=self.cleaned_data['Digits'])
            if user is None:
                raise forms.ValidationError(_('Bad password.'))
        
        return super(VerifyPasswordForm, self).clean()
    
class HandleDifferentPhoneForm(forms.Form):
    
    CallSid = forms.CharField(required=True)
    Digits = forms.CharField(required=False)
    
    def clean_Digits(self):
        if 'Digits' in self.cleaned_data and self.cleaned_data['Digits'] != '':
            phone = self.cleaned_data['Digits']
            if len(phone) == 10:
                phone = '%s-%s-%s' % (phone[0:3], phone[3:6], phone[6:10],)
                self.cleaned_data['Digits'] = phone
                
                try:
                    profile = ApplicantProfile.objects.get(mobile_number=phone)
                except ApplicantProfile.DoesNotExist:
                    raise forms.ValidationError(_('Number not found'))

        return self.cleaned_data['Digits']
    
class JobCodeFragmentForm(forms.Form):
    
    CallSid = forms.CharField(required=True)
    Digits = forms.CharField(required=False)
    
    def clean_Digits(self):
        if 'Digits' in self.cleaned_data and self.cleaned_data['Digits'] != '':
            try:
                job = Job.objects.get(job_code=self.cleaned_data['Digits'])
            except Job.DoesNotExist:
                raise forms.ValidationError(_('Bad job code.'))
            
        return self.cleaned_data['Digits']
