__author__ = 'phpdude'
__version__ = (0, 4, 0)

def correct_path(name, prefix):
    if name.startswith('/'):
        return name[1:]

    return "/".join((x.strip("/") for x in (prefix, name))).lstrip("/")


def process_response(response, tplname):
    tpl_name, processors = '', {}

    if response is None:
        response = tplname + ".html"
    elif isinstance(response, dict):
        response = (tplname + ".html", response)

    if isinstance(response, basestring):
        tpl_name = response
    elif isinstance(response, (tuple, list)):
        if not isinstance(response[0], basestring):
            response = (tplname + ".html",) + tuple(response)
        if len(response) == 2:
            tpl_name, processors = response
        elif len(response) == 3:
            tpl_name, processors, mimetype = response

    return tpl_name, processors


def render_template(template_name, context=None, instance=None):
    from django.conf import settings

    if getattr(settings, 'RENDER_ENGINE', 'django').lower() == 'coffin':
        from coffin.shortcuts import render_to_response
    else:
        from django.shortcuts import render_to_response

    return render_to_response(
        template_name,
        dictionary=context,
        context_instance=instance
    )
