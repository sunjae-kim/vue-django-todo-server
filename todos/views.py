from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TodoSerializer
from .models import Todo


@api_view(['GET', 'POST'])
def create_readlist(request):
    if request.method == 'GET':
        todos = Todo.objects.all()
        if request.GET.get('is-completed'):
            is_completed = bool(int(request.GET.get('is-completed')))
            todos = todos.filter(is_completed=is_completed)
        if request.GET.get('page'):
            page = int(request.GET.get('page'))
            limit = int(request.GET.get('limit', 5))
            todos = todos[(page-1)*limit:page*limit]
        serializer = TodoSerializer(todos, many=True)
    if request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    return Response(serializer.data)


@api_view(['GET', 'DELETE', 'PUT'])
def read_update_delete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    if request.method == 'GET':
        serializer = TodoSerializer(todo)
    if request.method == 'DELETE':
        serializer = TodoSerializer(todo)
        todo.delete()
    if request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.data) # or instance=todo
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    return Response(serializer.data)
