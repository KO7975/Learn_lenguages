from django.contrib import admin
from django.utils.safestring import mark_safe
from modeltranslation.admin import *
from django.views.decorators.csrf import csrf_exempt
from .models import (
    Language,
    LanguageLevel,
    Topic,
    Material,
    Course,
    Lesson,
    UserProfile,
    Commens,
)


class MaterialInline(admin.TabularInline):
    model = Material
    readonly_fields = ('id', 'material_tag' )
    classes = ('collapse', )
    extra = 0
    
@csrf_exempt
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'material_type', 'image_tag')
    search_fields = ('material_type','title',)

    def image_tag(self, obj):
        if obj.material_type == 'photo':
            return mark_safe(f'<img src="{obj.material_file.url}" width="50" height="60" />')
        else:
            return 'Not img'
        

class LessonsAdminInline(admin.TabularInline):
    model=Lesson
    extra = 0
    classes = ('collapse', )
    # raw_id_fields=['topic']
    filter_horizontal = ('materials',)
    # list_display = ('number', )
    # search_fields = ('number', 'materials')


class TopicAdmin(admin.ModelAdmin):
    inlines = [LessonsAdminInline, MaterialInline]
    # list_display = ('name', )
    search_fields = ('name',)
    # filter_horizontal = ('lesson',)

    
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title',)
    filter_horizontal = ('lesson1', 'materials')
    search_fields = ('title',)

    
class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    list_display = ('user','courses','is_approved',)
    list_filter = ('courses', 'is_approved')
    

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'time_created' )


admin.site.register(Lesson)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Language)
admin.site.register(LanguageLevel)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Commens, CommentsAdmin)
