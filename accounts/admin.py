from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, CandidateProfile, Company


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'phone', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Portal Role & Info', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Portal Role & Info', {'fields': ('role', 'phone', 'email', 'first_name', 'last_name')}),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'recruiter', 'location', 'industry', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'industry', 'created_at')
    search_fields = ('name', 'location', 'industry', 'recruiter__username', 'recruiter__email')
    actions = ['approve_companies', 'revoke_approval']

    @admin.action(description="Approve selected companies (allow recruiters to post jobs)")
    def approve_companies(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"Successfully approved {updated} company/companies.")

    @admin.action(description="Revoke approval for selected companies")
    def revoke_approval(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"Revoked approval for {updated} company/companies.")


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'headline', 'experience_years', 'skills', 'created_at')
    list_filter = ('experience_years', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'headline', 'skills')
