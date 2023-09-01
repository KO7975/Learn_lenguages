from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe


class Language(models.Model):
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.language


class LanguageLevel(models.Model):
    LEVEL_CHOICES = [
        ('ALL', 'ALL'),
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('C1', 'C1'),
        ('C2', 'C2'),
    ]
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES)

    def __str__(self):
        return f"{self.language} - {self.level}"


class Topic(models.Model):
    name = models.CharField(max_length=100,)
    level = models.ForeignKey(LanguageLevel, on_delete=models.CASCADE, null=True)
    # lesson = models.ManyToManyField('Lesson', blank=True)
    
    def __str__(self):
        return f'{self.name} - {self.level}'


class Lesson(models.Model):
    name = models.CharField( max_length=100, null=True,)
    number = models.IntegerField(null=True,)
    materials = models.ManyToManyField('Material', blank=True, related_name='lessonsm',)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE,null=True)

    def __str__(self):  
        return f"Lesson  {self.number} - {self.name} - {self.topic}"


def get_upload_path(instance, filename):
    return f'materials/{instance.material_type}/{filename}'


class Material(models.Model):
    title = models.CharField(max_length=80, null=True,)
    MATERIAL_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('text', 'Text'),
        ('url', 'Url')
    ]
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    material_type = models.CharField(max_length=5, choices=MATERIAL_CHOICES)
    material_file = models.FileField(upload_to=get_upload_path, null=True, blank=True, )
    url = models.CharField(max_length=150, blank=True, null=True)
    text = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:  # the material is being created
            if self.material_file is None:
                self.material_file.upload_to = get_upload_path(self, self.material_file.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.material_type} - {self.topic} - {self.title }"
    
    def material_tag(self):
        if self.material_file.url is not None:
            if self.material_type == 'photo':
                return mark_safe(f'<img width="320" height="auto" src="{self.material_file.url}" height="50"/>')
            elif self.material_type == 'video':
                return mark_safe(f'<video width="400"  controls><source src="{self.material_file.url}">')
            elif self.material_type == 'audio':
                return mark_safe(f'<audio controls><source src="{self.material_file.url}">')
        return ''


class Course(models.Model):
    title = models.CharField(max_length=50, null=True,)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    materials = models.ManyToManyField(Material, blank=True, related_name='coursesm')
    lesson1 = models.ManyToManyField(Lesson, blank=True, related_name='coursesl')

    def get_absolute_url(self):
        return reverse('course', kwargs={'course_id': self.pk})

    def __str__(self):
        return f"{self.title} - {self.topic}"
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    courses = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    phone = models.CharField(max_length=13, blank=True, null=True)

    def __str__(self):
        return f'User name: {self.user.last_name} {self.user.first_name}'
    

class Commens(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE, null=True,)
    comment = models.TextField( blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_appdated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Comment'
        ordering = ['-time_created']

