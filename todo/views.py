from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Tag, Task 
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from rest_framework.decorators import action

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'

class hashDict(dict):

    def __hash__(self):
        return hash(tuple(sorted(self.items())))


def index(request):

    return HttpResponse('Hello World!')

class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request):
        filtersQuery = self.request.query_params
        if filtersQuery:
            filters = dict(filtersQuery)['tag']
            tagIDs = []
            for tag in Tag.objects.filter(title__in=filters):
                tagIDs.append(tag.pk)
            tasks = Task.objects.filter(tag__in=tagIDs).distinct()
            serializer = TaskSerializer(tasks, many=True)
            if tasks:
                return Response(serializer.data)
            else:
                return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = TaskSerializer(self.queryset, many=True)
            return Response(serializer.data)
        



