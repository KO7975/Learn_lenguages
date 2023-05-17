from django import template
from materials.models import Course
import english_learning.settings as settings

register = template.Library()

@register.simple_tag(name='get_list_courses')
def get_course():
    return Course.objects.all()

@register.inclusion_tag('materials/templates/course_ditail.html')
def show_courses(arg1='Course', arg2='List'):
    categories = Course.objects.all()
    return {'courses': categories, 'arg1': arg1, 'arg2': arg2}

