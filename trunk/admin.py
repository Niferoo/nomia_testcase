from django.contrib import admin

from trunk.models import *


class TemplateFieldInline(admin.TabularInline):
    model = TemplateField
    prepopulated_fields = {'tag': ('title',)}
    fk_name = 'template'


class FieldParameterInline(admin.TabularInline):
    model = FieldParameter


@admin.register(TemplateField)
class TemplateFieldAdmin(admin.ModelAdmin):
    inlines = [FieldParameterInline]


@admin.register(FieldParameter)
class FieldParameterAdmin(admin.ModelAdmin):
    pass


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    pass


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    inlines = [TemplateFieldInline]
    save_as = True
    prepopulated_fields = {"tag": ("title",)}

