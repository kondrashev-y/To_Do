from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
import csv
from django.http import HttpResponse

from .custom_parser import CSVTextParser
from .serializers import TaskSerializer, TaskCreateSerializers, FileSerializer
from .models import Task
from .utils import UploadingTasks


def csv_file_parser(file):
    result_dict = {}
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        line_count = 1
        for rows in reader:
            for key, value in rows.items():
                if not value:
                    raise ParseError('Missing value in file. Check the {} line'.format(line_count))
            result_dict[line_count] = rows
            line_count += 1
    return result_dict


@api_view(['GET'])
def apiOverview(request):
    """Обзор API"""
    api_urls = {
        'List': '/task-list/',
        'Detail View': '/api-detail/<str:pk>/',
        'Create': '/task-create/',
        'Update': '/task-update/<str:pk>/',
        'Delete': '/task-delete/<str:pk>/',
        'Download': '/task-download/',
        'Uploads': '/task-uploads/',
    }
    return Response(api_urls)


class TaskListApiViews(ListAPIView):
    """Вывод списка задач в API"""

    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TaskDetailApiViews(RetrieveAPIView):
    """Вывод детальной информации по задаче в API"""

    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_field = 'pk'


class TaskUpdateApiViews(UpdateAPIView):
    """Изменение задачи"""

    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializers
    lookup_field = 'pk'


class TaskCreateApiViews(CreateAPIView):
    """Добавление задачи"""

    serializer_class = TaskCreateSerializers


class TaskDestroy(DestroyAPIView):
    """Удаление задачи"""
    queryset = Task.objects.all()


class CSVviewSet(APIView):
    """Отправка списка заданий в формате csv"""
    queryset = Task.objects.all()

    def get(self, request, format=None):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        writer = csv.DictWriter(response, fieldnames=['id', 'title', 'text', 'completed', 'finish_date', 'tag'])
        writer.writeheader()
        for task in self.queryset.all():
            tag_list = []
            for tag in task.tag.values_list():
                tag_list.append(tag[1])
            writer.writerow({'id': task.id, 'title': task.title, 'text': task.text,
                             'completed': task.completed, 'finish_date': task.finish_date,
                             'tag': ', '.join(tag_list)})
        response.status_code = status.HTTP_200_OK
        return response


class FileUploadView(APIView):
    parser_classes = (CSVTextParser,)
    serializer_class = FileSerializer

    def put(self, request, version=None):
        """Загрузка списка заданий в формате csv. Формат (id,title,text,completed,finish_date,tag)"""
        content_type = request.content_type.split(';')[0].strip()
        encoding = 'utf-8'

        if content_type == 'text/csv':
            csv_table = request.data
            uploding_file = UploadingTasks(csv_table)
            if uploding_file:
                return Response('Task_created', status.HTTP_201_CREATED)
            else:
                return Response('Error', status.HTTP_406_NOT_ACCEPTABLE)
        elif content_type == 'multipart/form-data':
            fh = request.data.get('file', None)
            csv_table = fh.read().decode(encoding)
            return Response(csv_table, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)