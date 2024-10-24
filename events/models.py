# events/models.py
from django.db import models
from django.urls import reverse
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hosted_events')
    isFeatured=models.BooleanField(default=False)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:detail', args=[str(self.id)])
    

# events/models.py



class Registration(models.Model):
    DEPARTMENT_CHOICES = [
        ('CS', 'Computer Science'),
        ('IT', 'Information Technology'),
        ('ECE', 'Electronics and Communication'),
        ('EEE', 'Electrical and Electronics'),
        ('ME', 'Mechanical Engineering'),
        # Add more departments as needed
    ]

    SEMESTER_CHOICES = [
        ('1', '1st Semester'),
        ('2', '2nd Semester'),
        ('3', '3rd Semester'),
        ('4', '4th Semester'),
        ('5', '5th Semester'),
        ('6', '6th Semester'),
        ('7', '7th Semester'),
        ('8', '8th Semester'),
    ]

    COURSE_CHOICES = [
        ('BTech', 'Bachelor of Technology'),
        ('MTech', 'Master of Technology'),
        ('MCA', 'Master of Computer Applications'),
        ('BCA', 'Bachelor of Computer Applications'),
        # Add more courses as needed
    ]

    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_registrations')
    department = models.CharField(max_length=3, choices=DEPARTMENT_CHOICES)
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)
    course = models.CharField(max_length=5, choices=COURSE_CHOICES)
    college = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"