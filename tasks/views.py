from django.shortcuts import render, redirect
from django.http import JsonResponse
# Create your views here.
from .models import Task
from .forms import TaskForm

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            print("Form valid")
            form.save()
            return redirect('task_list')
        else:
            print(form.errors)
            print(form.cleaned_data)
    else:
        form = TaskForm()
    return render(request, 'tasks/task_create.html', {'form': form})

def task_update(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_update.html', {'form': form, 'task': task})

def task_delete(request, pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    return redirect('task_list')

def update_task_status(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id")
        column_id = request.POST.get("column_id")

        try:
            task = Task.objects.get(pk=task_id)
            task.status = column_id
            task.save()

            return JsonResponse({"message": "Task status updated successfully.", "status": task.status})
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found."})
    else:
        return JsonResponse({"error": "Invalid request method."})
