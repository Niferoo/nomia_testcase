from django.db import models
from django.utils.translation import gettext


class Template(models.Model):
    tag = models.SlugField(max_length=100, unique=True, verbose_name=('Тег'))
    title = models.CharField(max_length=50, verbose_name=('Название шаблона'))
    text = models.TextField(max_length=500,blank=True, null=True, verbose_name=('Текст шаблона'))

    def __str__(self):
        return self.title

    def fields(self):
        return TemplateField.objects.filter(template=self).order_by('tab')

    def __unicode__(self):
        return self.title


class TemplateField(models.Model):
    FieldTypes = (('T', 'Text'), ('B', 'Bool'), ('E', 'E-mail'),
                  ('U', 'URL'), ('C', 'Choices'), ('M', 'Multichoice'),)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, verbose_name="Шаблон")
    tag = models.SlugField(max_length=100, unique=True, blank=False, null=False, verbose_name="Тег")
    title = models.CharField(max_length=255, verbose_name="Название поля")
    type = models.CharField(max_length=1, choices=FieldTypes, verbose_name="Тип")
    tab = models.IntegerField(default=0, verbose_name="Место поля")
    required = models.BooleanField(default=True, verbose_name="Обязательное")
    next_template = models.ForeignKey(Template,
        on_delete=models.CASCADE,
        related_name='previous_template_field',
        blank=True,
        null=True,
        verbose_name="Следующий шаблон")

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u'%s: %s' % (self.template, self.tag)

    def parameters(self):
        return FieldParameter.objects.filter(field=self).order_by('tab')

    class Meta:
        unique_together = ("template", "tag")


class FieldParameter(models.Model):
    field = models.ForeignKey(TemplateField, on_delete=models.CASCADE, verbose_name="Поле")
    tag = models.SlugField(max_length=100, unique=True, blank=False, null=False, verbose_name="Тег")
    value = models.CharField(max_length=255, verbose_name="Значение")
    tab = models.IntegerField(default=0, verbose_name="Место поля")

    def __str__(self):
        return self.field

    def __unicode__(self):
        return u'%s: %s = %s' % (self.field, self.tag, self.value)

    class Meta:
        unique_together = ("field", "tag", "value")


class Record(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    dt = models.DateTimeField()

    def __str__(self):
        return self.template.title

    def __unicode__(self):
        return u'%s @ %s' % (self.template, self.dt)

        def data(self):
            return RecordData.objects.filter(record=self).order_by('field__tab')


class RecordData(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, verbose_name="Запись")
    field = models.ForeignKey(TemplateField, on_delete=models.CASCADE, verbose_name="Поле")
    value = models.TextField(verbose_name='Значение')

    def __str__(self):
        return self.record

    def __unicode__(self):
        return u'%s %s' % (self.record, self.field)

    class Meta:
        unique_together = ("record", "field")

    def decoded_value(self):
        if self.field.type == 'M':
            return eval(self.value)
        return self.value

    def rendered_value(self):
        if self.field.type == 'B':
            if self.value == 'True':
                return gettext("Yes")
            elif self.value == 'False':
                return gettext("No")
        return self.value
