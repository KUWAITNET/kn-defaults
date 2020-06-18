from django.contrib.contenttypes.models import ContentType


def cms_plugin_change_admin_log(sender, operation, request, language, token, origin, **kwargs):
    from cms.models import CMSPlugin
    operation = operation
    data = ''

    from django.contrib.admin.models import LogEntry
    if operation == 'paste_plugin':
        placeholder = kwargs.get('target_placeholder', False)
    else:
        placeholder = kwargs.get('placeholder', False)

    if not placeholder:
        return

    pk = placeholder.pk

    if 'change' in operation:
        action_flag = '2'
        data = {}
        old_plugin = kwargs['old_plugin'].__dict__
        new_plugin = kwargs['new_plugin'].__dict__
        pk = new_plugin['id']
        for key, val in old_plugin.items():
            if not key.startswith('_') and not key == 'changed_date':
                new_value = new_plugin.get(key)
                if new_value != val:
                    data[key] = {'old': val, 'new': new_value}

    elif 'add' in operation:
        action_flag = '1'
    else:
        action_flag = '3'

    LogEntry.objects.create(
        user=request.user,
        content_type=ContentType.objects.get_for_model(CMSPlugin),
        object_id=pk,
        object_repr=str(placeholder),
        action_flag=action_flag,
        change_message=f'{data}',
    )
