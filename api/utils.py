import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'to_do.settings'

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import django
django.setup()

from api.models import Task


class UploadingTasks(object):
    """Загрузка списка задач"""
    m2m_key_fields = ['tag']
    model = Task

    def __init__(self, lst):
        self.lst = lst
        self.parsing()

    def getting_related_model(self, field_name):
        related_model = self.model._meta.get_field(field_name).related_model
        return related_model

    def parsing(self):
        headers = self.lst[0]
        for row in self.lst[1:]:
            row_dict = {}
            tag_instance_list = []
            for column in range(len(headers)):
                value = row[column]
                field_name = headers[column]
                if field_name == 'id':
                    continue

                if field_name in self.m2m_key_fields:
                    related_model = self.getting_related_model(field_name)
                    tag_list = value.split(', ')
                    if tag_list[0]:
                        for tag in tag_list:
                            instance, crated = related_model.objects.get_or_create(name=tag, slug=tag)
                            tag_instance_list.append(instance)
                    continue

                row_dict[field_name] = value

            new_task = Task.objects.create(**row_dict)
            if tag_instance_list:
                new_task.tag.add(*tag_instance_list)
                new_task.save()

        return True

