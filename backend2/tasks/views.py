import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Task
from .serializers import TaskSerializer
from django.http import HttpResponse
from openpyxl import Workbook

JWT_SECRET = 'super_secret_key'  # Must match Node backend

def get_user_from_token(request):
    auth = request.headers.get('Authorization', '').split()
    if len(auth) != 2:
        return None
    try:
        decoded = jwt.decode(auth[1], JWT_SECRET, algorithms=["HS256"])
        return decoded.get('id')
    except Exception:
        return None

class TaskListCreateView(APIView):
    def get(self, request):
        user_id = get_user_from_token(request)
        if not user_id:
            return Response({'detail': 'Unauthorized'}, status=401)
        tasks = Task.objects.filter(user_id=user_id)
        return Response(TaskSerializer(tasks, many=True).data)

    def post(self, request):
        user_id = get_user_from_token(request)
        if not user_id:
            return Response({'detail': 'Unauthorized'}, status=401)
        data = request.data.copy()
        data['user_id'] = user_id
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class TaskDetailView(APIView):
    def put(self, request, pk):
        user_id = get_user_from_token(request)
        try:
            task = Task.objects.get(pk=pk, user_id=user_id)
        except Task.DoesNotExist:
            return Response({'detail': 'Not found'}, status=404)
        data = request.data.copy()
        data['user_id'] = user_id
        serializer = TaskSerializer(task, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        user_id = get_user_from_token(request)
        try:
            task = Task.objects.get(pk=pk, user_id=user_id)
            task.delete()
            return Response(status=204)
        except Task.DoesNotExist:
            return Response({'detail': 'Not found'}, status=404)

class TaskExportExcelView(APIView):
    def get(self, request):
        user_id = get_user_from_token(request)
        if not user_id:
            return Response({'detail': 'Unauthorized'}, status=401)

        tasks = Task.objects.filter(user_id=user_id)

        wb = Workbook()
        ws = wb.active
        ws.title = "Tasks"
        ws.append(['Title', 'Description', 'Effort', 'Due Date', 'Created At'])

        for task in tasks:
            ws.append([task.title, task.description, task.effort, task.due_date.isoformat(), task.created_at.isoformat()])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=tasks.xlsx'
        wb.save(response)
        return response
