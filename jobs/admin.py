from django.contrib import admin
from .models import Job, Application, SavedJob


class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0
    fields = ('candidate', 'status', 'resume', 'applied_at')
    readonly_fields = ('applied_at',)
    can_delete = True


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'recruiter', 'location', 'job_type', 'is_active', 'views_count', 'created_at')
    list_filter = ('job_type', 'is_active', 'created_at', 'company')
    search_fields = ('title', 'skills_required', 'location', 'company__name', 'recruiter__username')
    inlines = [ApplicationInline]
    actions = ['activate_jobs', 'deactivate_jobs']

    @admin.action(description="Mark selected jobs as Active")
    def activate_jobs(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} job(s) marked as active.")

    @admin.action(description="Mark selected jobs as Inactive (Remove spam / expired)")
    def deactivate_jobs(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} job(s) deactivated.")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'status', 'applied_at', 'updated_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('candidate__username', 'candidate__email', 'job__title', 'job__company__name')
    actions = ['shortlist_applications', 'reject_applications']

    @admin.action(description="Set status to Shortlisted for selected applications")
    def shortlist_applications(self, request, queryset):
        updated = queryset.update(status=Application.Status.SHORTLISTED)
        self.message_user(request, f"{updated} application(s) shortlisted.")

    @admin.action(description="Set status to Rejected for selected applications")
    def reject_applications(self, request, queryset):
        updated = queryset.update(status=Application.Status.REJECTED)
        self.message_user(request, f"{updated} application(s) rejected.")


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'saved_at')
    search_fields = ('candidate__username', 'job__title', 'job__company__name')
