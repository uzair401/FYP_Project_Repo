# students/decorators.py
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def is_editor(user):
    if user.groups.filter(name='editor').exists():
        return True
    else:
        raise PermissionDenied

editor_required = user_passes_test(is_editor)
