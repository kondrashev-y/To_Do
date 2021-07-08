from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify
from rest_framework import serializers

from .models import Task, Tag


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug


def create_tag_list(tags_str):
    tags_str = tags_str.split(' ')
    tag_list = list()
    if tag_list:
        for tag_str in tags_str:
            try:
                tag = Tag.objects.get(slug=gen_slug(tag_str))
            except ObjectDoesNotExist:

                tag = Tag(slug=gen_slug(tag_str), name=gen_slug(tag_str))
            tag.save()
            tag_list.append(tag)
    return tag_list


class TagSerializer(serializers.ModelSerializer):
    """Список тегов"""

    class Meta:
        model = Tag
        fields = ('name',)


class TaskSerializer(serializers.ModelSerializer):

    tag = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializers(serializers.ModelSerializer):

    tags = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Task
        fields = ('title', 'text', 'completed', 'finish_date', 'tags', )


    def validate_tags(self, value):
        """
        Добавление списка тэгов
        """
        tags_list = create_tag_list(value)
        return tags_list

    def create(self, validated_data):
        task = Task.objects.create(
            title=validated_data.get('title', None),
            text=validated_data.get('text', None),
            finish_date=validated_data.get('finish_date', None),
        )
        task.save()
        task.tag.set(validated_data.get('tags', None))
        task.save()
        return task


class FileSerializer(serializers.ModelSerializer):

    file = serializers.FileField()

    class Meta:

        model = Task
        fields = ('file',)