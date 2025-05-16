from django.db import models
from django.utils import timezone

class BaseContent(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class HomePage(BaseContent):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    hero_title = models.CharField(max_length=200)
    hero_subtitle = models.TextField()
    featured_image = models.ImageField(upload_to='home/', null=True, blank=True)

    def __str__(self):
        return "Home Page Content"

class AboutPage(BaseContent):
    mission = models.TextField()
    vision = models.TextField()
    team_image = models.ImageField(upload_to='about/', null=True, blank=True)

    def __str__(self):
        return "About Page Content"

class ContactPage(models.Model):
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "Contact Page Content"

class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('membership', 'Membership Information'),
        ('events', 'Events & Programs'),
        ('feedback', 'Feedback'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_messages'
    )
    notes = models.TextField(blank=True, help_text="Admin notes about the resolution")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} - {self.get_subject_display()} ({self.created_at.strftime('%Y-%m-%d')})"

    def mark_as_resolved(self, user, notes=''):
        self.is_resolved = True
        self.resolved_at = timezone.now()
        self.resolved_by = user
        self.notes = notes
        self.save()

    def mark_as_unresolved(self):
        self.is_resolved = False
        self.resolved_at = None
        self.resolved_by = None
        self.notes = ''
        self.save()

class EventsPage(BaseContent):
    event_date = models.DateField()
    event_location = models.CharField(max_length=200)
    event_image = models.ImageField(upload_to='events/', null=True, blank=True)
    long_description = models.TextField(null=True, blank=True, help_text="Detailed description of the event")

    def __str__(self):
        return f"Event: {self.title}"

class EventImage(models.Model):
    event = models.ForeignKey(EventsPage, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.event.title}"

class MembersPage(BaseContent):
    SOCIETY_DESIGNATION_CHOICES = [
        ('PRESIDENT', 'President'),
        ('VICE_PRESIDENT', 'Vice President'),
        ('GENERAL_SECRETARY', 'General Secretary'),
        ('SECRETARY', 'Secretary'),
        ('TREASURER', 'Treasurer'),
        ('EXECUTIVE_MEMBER', 'Executive Member'),
        ('GENERAL_MEMBER', 'General Member'),
    ]

    member_name = models.CharField(max_length=200)
    member_position = models.CharField(max_length=200, help_text="Academic/Professional position")
    member_image = models.ImageField(upload_to='members/', null=True, blank=True)
    member_bio = models.TextField(null=True,default=None)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True, help_text="Contact phone number")
    date_of_joining = models.DateField(null=True, default=None)
    society_designation = models.CharField(
        max_length=50,
        choices=SOCIETY_DESIGNATION_CHOICES,
        default='GENERAL_MEMBER'
    )

    class Meta:
        ordering = ['society_designation', 'member_name']
        verbose_name = 'Member'
        verbose_name_plural = 'Members'

    @property
    def is_executive_member(self):
        return self.society_designation != 'GENERAL_MEMBER'

    def __str__(self):
        return f"{self.member_name} - {self.get_society_designation_display()}"

class GalleryPage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=200,null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return self.caption

class JoinPage(BaseContent):
    benefits = models.TextField()
    requirements = models.TextField()
    application_form_embed = models.TextField(help_text="Embed code for application form")

    def __str__(self):
        return "Join Page Content"

class PresidentMessage(BaseContent):
    president_name = models.CharField(max_length=200)
    president_image = models.ImageField(upload_to='president/', null=True, blank=True)
    designation = models.CharField(max_length=200)
    message = models.TextField(null=True)

    def __str__(self):
        return f"President Message: {self.president_name}"

class Update(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)  # Higher number means higher priority
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return self.title


