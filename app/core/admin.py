from django.contrib import admin
from django.contrib import messages
from django.utils import timezone

from .forms import HomePageForm
from .models import (
    HomePage, AboutPage, ContactPage, EventsPage, EventImage,
    MembersPage, GalleryPage, JoinPage, PresidentMessage,
    Update, ContactMessage
)

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    form = HomePageForm

    list_display = ('name','description','title','last_updated', 'is_active')
    search_fields = ('title', 'content')


    
    def has_add_permission(self, request):
        # Only allow adding if no instance exists
        return not HomePage.objects.exists()

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'last_updated', 'is_active')
    search_fields = ('title', 'content', 'mission', 'vision')
    
    def has_add_permission(self, request):
        # Only allow adding if no instance exists
        return not AboutPage.objects.exists()

@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ( 'email', 'phone')
    search_fields = ( 'content', 'address', 'email')

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1
    fields = ('image', 'caption', 'order')

@admin.register(EventsPage)
class EventsPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'event_location', 'last_updated', 'is_active')
    list_filter = ('event_date', 'is_active')
    search_fields = ('title', 'content', 'event_location', 'long_description')
    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'event_date', 'event_location', 'is_active')
        }),
        ('Content', {
            'fields': ('content', 'long_description')
        }),
        ('Featured Image', {
            'fields': ('event_image',),
            'description': 'Main event image. Additional images can be added below.'
        }),
    )
    inlines = [EventImageInline]
    date_hierarchy = 'event_date'

@admin.register(MembersPage)
class MembersPageAdmin(admin.ModelAdmin):
    list_display = ('member_name', 'society_designation', 'member_position', 'email', 'phone_number', 'date_of_joining', 'is_active')
    list_filter = ('society_designation', 'is_active')
    search_fields = ('member_name', 'member_position', 'email', 'phone_number')
    date_hierarchy = 'date_of_joining'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('member_name', 'email', 'phone_number', 'member_position', 'member_image')
        }),
        ('Society Details', {
            'fields': ('society_designation', 'date_of_joining')
        }),
        ('Additional Information', {
            'fields': ('member_bio', 'is_active')
        }),
    )

@admin.register(GalleryPage)
class GalleryPageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('caption',)

@admin.register(JoinPage)
class JoinPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'last_updated', 'is_active')
    search_fields = ('title', 'content', 'benefits', 'requirements')
    
    def has_add_permission(self, request):
        # Only allow adding if no instance exists
        return not JoinPage.objects.exists()

@admin.register(PresidentMessage)
class PresidentMessageAdmin(admin.ModelAdmin):
    list_display = ('president_name', 'designation', 'last_updated')
    search_fields = ('president_name', 'content', 'designation')
    
    def has_add_permission(self, request):
        # Only allow adding if no instance exists
        return not PresidentMessage.objects.exists()

@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'priority', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'priority', 'created_at')
    search_fields = ('title', 'content')
    list_editable = ('is_active', 'priority')
    ordering = ('-priority', '-created_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Update Content', {
            'fields': ('title', 'content')
        }),
        ('Settings', {
            'fields': ('is_active', 'priority'),
            'description': 'Control the visibility and importance of the update. Higher priority numbers will be highlighted.'
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject_display', 'created_at', 'is_resolved', 'resolved_by', 'resolved_at')
    list_filter = ('is_resolved', 'subject', 'created_at')
    search_fields = ('name', 'email', 'message', 'notes')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Message Details', {
            'fields': ('name', 'email', 'subject', 'message', 'created_at')
        }),
        ('Resolution Status', {
            'fields': ('is_resolved', 'resolved_at', 'resolved_by', 'notes'),
            'classes': ('collapse',),
            'description': 'Message resolution status and admin notes'
        }),
    )

    def subject_display(self, obj):
        return obj.get_subject_display()
    subject_display.short_description = 'Subject'

    actions = ['mark_resolved', 'mark_unresolved']

    def mark_resolved(self, request, queryset):
        for message in queryset.filter(is_resolved=False):
            message.mark_as_resolved(request.user)
        count = queryset.filter(is_resolved=False).count()
        self.message_user(request, f'{count} message(s) marked as resolved.')
    mark_resolved.short_description = 'Mark selected messages as resolved'

    def mark_unresolved(self, request, queryset):
        for message in queryset.filter(is_resolved=True):
            message.mark_as_unresolved()
        count = queryset.filter(is_resolved=True).count()
        self.message_user(request, f'{count} message(s) marked as unresolved.')
    mark_unresolved.short_description = 'Mark selected messages as unresolved'

    def save_model(self, request, obj, form, change):
        if 'is_resolved' in form.changed_data:
            if obj.is_resolved:
                obj.resolved_at = timezone.now()
                obj.resolved_by = request.user
            else:
                obj.resolved_at = None
                obj.resolved_by = None
        super().save_model(request, obj, form, change)

