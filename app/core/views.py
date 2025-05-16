from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from .models import (
    HomePage, AboutPage, ContactPage, EventsPage,
    MembersPage, GalleryPage, JoinPage, PresidentMessage,
    Update, ContactMessage
)


def home_view(request):
    events = EventsPage.objects.all()[:5]  # Get latest 5 events
    updates = Update.objects.filter(is_active=True)  # Get all active updates
    contact_content = ContactPage.objects.first()
    
    context = {
        'events': events,
        'updates': updates,
        'contact_content': contact_content,
    }
    return render(request, 'index.html', context)


def about_view(request):
    """Render the about page."""
    context = {
        'about_content': AboutPage.objects.filter(is_active=True).first()
    }
    return render(request, 'about.html', context)


def events_view(request):
    """Render the events page."""
    now = timezone.now().date()
    contact_content = ContactPage.objects.first()
    
    context = {
        'events': EventsPage.objects.filter(is_active=True).order_by('-event_date'),
        'now': now,
        'contact_content': contact_content,
    }
    return render(request, 'events.html', context)


def members_view(request):
    """Render the members page."""
    contact_content = ContactPage.objects.first()
    
    context = {
        'members': MembersPage.objects.filter(is_active=True),
        'contact_content': contact_content,
    }
    return render(request, 'members.html', context)


def gallery_view(request):
    """Render the gallery page."""
    contact_content = ContactPage.objects.first()
    
    context = {
        'gallery_items': GalleryPage.objects.filter(is_active=True),
        'contact_content': contact_content,
    }
    return render(request, 'gallery.html', context)


def join_view(request):
    """Handle membership application form."""
    contact_content = ContactPage.objects.first()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        designation = request.POST.get('designation')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        if all([name, designation, email]):
            try:
                MembersPage.objects.create(
                    member_name=name,
                    member_position=designation,
                    email=email,
                    phone_number=phone,
                    is_active=False,
                    society_designation='GENERAL_MEMBER',
                    title=f"Membership Application - {name}",
                    content=f"Application received from {name} for position {designation}"
                )
                messages.success(request, 'Your membership application has been submitted successfully. We will review it and get back to you soon.')
                return redirect('join')
            except Exception as e:
                messages.error(request, 'This email is already registered. Please use a different email address.')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'join.html', {
        'contact_content': contact_content
    })


def contact_view(request):
    contact_content = ContactPage.objects.first()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')
        
        if all([name, email, subject, message_text]):
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message_text
            )
            messages.success(request, 'Your message has been sent successfully. We will get back to you shortly.')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'contact.html', {
        'contact_content': contact_content
    })


def president_message_view(request):
    """Render the president message page."""
    contact_content = ContactPage.objects.first()
    
    context = {
        'president_message': PresidentMessage.objects.filter(is_active=True).first(),
        'contact_content': contact_content,
    }
    return render(request, 'president-message.html', context)