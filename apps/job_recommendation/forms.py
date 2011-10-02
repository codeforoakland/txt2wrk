from django import forms

from models import JobRecommendation
from applicant.models import ApplicantProfile
from job.models import Job

class JobRecommendationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(JobRecommendationForm, self).__init__(*args, **kwargs)

        self.fields['state'].widget = forms.HiddenInput()
        self.fields['job'].queryset = Job.objects.all()
        self.fields['applicant'].queryset = ApplicantProfile.objects.all()

    class Meta:
        model = JobRecommendation
