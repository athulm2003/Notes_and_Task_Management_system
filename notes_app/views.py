from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from notes_app.serializers import RegisterSerializer,NotesSerializer,TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from notes_app.models import NotesDb,TaskDb


# Create your views here.
class Registrationiew(APIView):
    def post(self,request):
        serializer_instance=RegisterSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={
                "Message" : "Registration Successful...!"
            })
        else:
            return Response(data=serializer_instance.errors)

class NotesListCreateView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        notes=NotesDb.objects.filter(user=request.user)
        serializer_instance=NotesSerializer(notes,many=True)
        return Response(serializer_instance.data)

    def post(self,request):
        serializer_instance=NotesSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)

class NotesRetrieveUpdateDeleteView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,pk):
        note_obj=get_object_or_404(NotesDb,id=pk,user=request.user)
        serializer_instance=NotesSerializer(note_obj)
        return Response(data=serializer_instance.data)

    def put(seslf,request,pk):
        note_obj=get_object_or_404(NotesDb,id=pk,user=request.user)
        serializer_instance=NotesSerializer(note_obj,data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={
                "Message" : "Notes Successfully Updated..!",
                "Updated_data" : serializer_instance.data
            })
        else:
            return Response(data=serializer_instance.errors)

    def delete(self,request,pk):
        note_obj=get_object_or_404(NotesDb,id=pk,user=request.user)
        note_obj.delete()
        return Response("Notes Deleted Successfully...!")

class LogoutView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        request.user.auth_token.delete()
        return Response({
            "Message": "Logout Success..!"
        })


class TaskListCreateView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        tasks=TaskDb.objects.filter(user=request.user)
        serializer_instance=TaskSerializer(tasks,many=True)
        return Response(serializer_instance.data)

    def post(self,request):
        serializer_instance=TaskSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class TaskRetrieveUpdateDeleteView(APIView):
    permission_classes=[IsAuthenticated]

    def get_task(self,request,id):
        return get_object_or_404(TaskDb,id=id,user=request.user)

    def get(self,request,id):
        task_obj=self.get_task(request,id)
        serializer_instance=TaskSerializer(task_obj)
        return Response(data=serializer_instance.data)
    
    def put(self,request,id):
        task_obj=self.get_task(request,id)
        serializer_instance=TaskSerializer(task_obj,request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={
                "Message" : "Task Updated Successfully...!",
                "Updated_Task" : serializer_instance.data
            })
        else:
            return Response(data=serializer_instance.errors)

    def delete(self,request,id):
        task_obj=self.get_task(request,id)
        task_obj.delete()
        return Response("Task Deleted Successfully...!")