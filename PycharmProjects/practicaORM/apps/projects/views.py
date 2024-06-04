from django.shortcuts import render

# Other modules.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

# Self modules.
from .models import *
from .serializers import ProjectSerializer, ProjectSerializerModel, TaskSerializer, CommentSerializer

#Utils
from datetime import datetime



class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializerModel

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ProjectAPIView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        project = Project()
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({})

    def delete(self, request):
        id= request.data.get('id', '')
        project = Project.objects.get(id=id)
        project.delete()
        return Response({})

    def patch(self, request):
        id= request.data.get('id', '')
        project = Project.objects.get(id=id)
        project.name = request.data.get('name', project.name)
        project.save()
        return Response({
            'id': project.id,
            'name': project.name
        })


class TaskAPIView(APIView):
    def get(self, request, project_id):
        tasks = Task.objects.filter(project__id=project_id)
        data = [
            {
                'id': task.id,
                'description': task.description,
                'end_date': task.end_date,
                'priority': task.priority
            }
            for task in tasks
        ]
        return Response(data)

    def post(self, request, project_id):
        task = Task()
        task.description = request.data.get('description', '')
        task.end_date = datetime.strptime(request.data.get('end_date', ''), '%d-%m-%YT%H:%M:%S')
        task.project = Project.objects.get(id=project_id)
        task.priority = request.data.get('priority', 'LOW')
        task.save()
        return Response({})

    def delete(self, request, project_id):
        id = request.data.get('id', '')
        task = Task.objects.get(id=id, project__id=project_id)
        task.delete()
        return Response({})

    def patch(self, request, project_id):
        id = request.data.get('id', '')
        task = Task.objects.get(id=id, project__id=project_id)
        task.description = request.data.get('description', task.description)
        task.end_date = datetime.strptime(request.data.get('end_date', ''), '%d-%m-%YT%H:%M:%S')
        task.priority = request.data.get('priority', task.priority)
        task.save()
        return Response({
            'id': task.id,
            'description': task.description,
            'end_date': task.end_date,
            'priority': task.priority
        })


