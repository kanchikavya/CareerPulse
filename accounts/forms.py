from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, CandidateProfile, Company
from .validators import validate_pdf_extension, validate_file_size


class CandidateRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    headline = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Python & Django Developer'}))
    skills = forms.CharField(max_length=500, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Python, Django, React, SQL'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.CANDIDATE
        if commit:
            user.save()
            CandidateProfile.objects.create(
                user=user,
                headline=self.cleaned_data.get('headline', ''),
                skills=self.cleaned_data.get('skills', '')
            )
        return user


class RecruiterRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Work Email Address'}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    company_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}))
    company_type = forms.ChoiceField(choices=Company.CompanyType.choices, required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    company_location = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Bengaluru, India or Remote'}))
    company_website = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://company.com'}))
    industry = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. FinTech, E-commerce, EdTech'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.RECRUITER
        if commit:
            user.save()
            Company.objects.create(
                recruiter=user,
                name=self.cleaned_data.get('company_name'),
                company_type=self.cleaned_data.get('company_type', Company.CompanyType.PRODUCT),
                location=self.cleaned_data.get('company_location'),
                website=self.cleaned_data.get('company_website', ''),
                industry=self.cleaned_data.get('industry', ''),
                is_approved=False
            )
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class CandidateProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CandidateProfile
        fields = (
            'headline', 'skills', 'experience_years', 'education',
            'bio', 'resume', 'portfolio_url', 'linkedin_url', 'github_url'
        )
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Senior Backend Engineer'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, PostgreSQL, Docker, AWS'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'education': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'B.Tech in Computer Science'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell recruiters about yourself and your journey...'}),
            'resume': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://yourportfolio.dev'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/username'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['phone'].initial = self.instance.user.phone

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
            profile.save()
        return profile


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'company_type', 'description', 'website', 'location', 'industry', 'logo')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'industry': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
