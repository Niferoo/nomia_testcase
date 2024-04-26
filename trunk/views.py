from django.shortcuts import render, redirect

from trunk.forms import *


def cdbform(request, template):
    _template = Template.objects.get(tag=template)
    template_text = _template.text
    if request.method == 'POST':
        form = CDBForm(template=template, data=request.POST)

        if form.is_valid():
            data = form.save()

            for key, value in request.POST.items():
                print(key, value)
                if value == 'on' or value != '':
                    print('da')

                    template_field = data.template.fields().filter(tag=key).first()
                    if template_field:
                        next_template_tag = template_field.next_template.tag if template_field.next_template else None
                        redirect_url = f'/form/{next_template_tag}/' if next_template_tag else '/'

                        if next_template_tag:
                            return redirect(redirect_url)
                        else:
                            data = form.save()

                            return render(request, 'sample.html', {'data': data,
                                                                                        'template_text': template_text,})
    else:
        form = CDBForm(template=template)
        context = {'form': form,
                   'template_text': template_text}
        return render(request, 'sample.html', context)