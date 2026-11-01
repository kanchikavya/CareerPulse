from django import forms
from .models import Job, Application


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = (
            'title', 'location', 'job_type', 'salary_min', 'salary_max',
            'skills_required', 'experience_required_years', 'deadline',
            'description', 'responsibilities', 'is_active'
        )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Senior Python / Django Engineer'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Bangalore, Mumbai, or Remote'}),
            'job_type': forms.Select(attrs={'class': 'form-select'}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 600000'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1200000'}),
            'skills_required': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Python, Django, REST API, PostgreSQL'}),
            'experience_required_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'e.g. 2'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Provide an overview of the role and what the team does...'}),
            'responsibilities': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '- Build high-performance REST APIs\n- Write unit and integration tests\n- Collaborate with frontend devs'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ApplicationForm(forms.ModelForm):
    use_profile_resume = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'use_profile_resume_checkbox'}),
        help_text="Use the resume already saved in your candidate profile"
    )

    class Meta:
        model = Application
        fields = ('resume', 'cover_letter')
        widgets = {
            'resume': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf', 'id': 'resume_file_input'}),
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share why you are an ideal fit for this role and any relevant achievements...'
            }),
        }

    def __init__(self, *args, candidate_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.candidate_profile = candidate_profile
        # If candidate already has a resume on profile, making upload optional
        if candidate_profile and candidate_profile.resume:
            self.fields['resume'].required = False
        else:
            self.fields['use_profile_resume'].initial = False
            self.fields['use_profile_resume'].widget.attrs['disabled'] = 'disabled'
            self.fields['resume'].required = True

    def clean(self):
        cleaned_data = super().clean()
        use_profile = cleaned_data.get('use_profile_resume')
        resume = cleaned_data.get('resume')

        if not use_profile and not resume:
            self.add_error('resume', 'Please upload a PDF resume for this application.')

        return cleaned_data


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('status', 'recruiter_notes')
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'recruiter_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional internal notes or feedback for candidate...'
            }),
        }
