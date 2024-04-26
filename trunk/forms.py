from datetime import datetime
from django import forms

from trunk.models import *


class CDBForm(forms.Form):
    def __init__(self, template=None, tag=None, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        if template:
            self.template = Template.objects.get(tag=template)  # template
        elif tag:
            self.template = Template.objects.get(tag=tag)
        fields = self.template.fields()
        for field in fields:
            widget = None
            help_text = ""
            for parameter in field.parameters():
                if parameter.tag == "widget":
                    if parameter.value == "textarea":
                        widget = forms.Textarea(attrs={'style': 'width: 350px;'})
                elif parameter.tag == "help_text":
                    help_text = parameter.value
            if field.type == "B":
                self.fields[field.tag] = forms.BooleanField(label=field.title,
                                                            required=field.required,
                                                            help_text=help_text)
            elif field.type == "T":
                if widget is None:
                    widget = forms.TextInput(attrs={'style': 'width: 350px;'})
                self.fields[field.tag] = forms.CharField(label=field.title,
                                                         required=field.required,
                                                         widget=widget)
            elif field.type == "C":
                choices = [('', '-')]
                for parameter in field.parameters():
                    if parameter.tag == "choice":
                        choices.append((parameter.value, parameter.value))
                self.fields[field.tag] = forms.ChoiceField(choices=choices,
                                                           label=field.title,
                                                           required=field.required)
            elif field.type == "M":
                choices = []
                for parameter in field.parameters():
                    if parameter.tag == "choice":
                        choices.append((parameter.value, parameter.value))
                self.fields[field.tag] = forms.MultipleChoiceField(choices=choices,
                                                                   label=field.title,
                                                                   widget=forms.CheckboxSelectMultiple,
                                                                   required=field.required)
            elif field.type == "E":
                self.fields[field.tag] = forms.EmailField(label=field.title, required=field.required)
            elif field.type == "U":
                widget = forms.TextInput(attrs={'style': 'width: 350px;'})
                self.fields[field.tag] = forms.URLField(label=field.title, required=field.required, widget=widget)

    def save(self, commit=True):
        data = self.cleaned_data
        rec = Record(template=self.template, dt=datetime.now())
        if commit:
            rec.save()
            for k, v in data.items():
                f = TemplateField.objects.get(template=self.template, tag=k)
                d = RecordData(record=rec, field=f, value=('%s' % v))
                d.save()
        return rec
