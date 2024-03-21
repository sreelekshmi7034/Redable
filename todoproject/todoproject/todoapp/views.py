from Tools.scripts.make_ctype import method
from django.shortcuts import render, redirect
from .models import Task
from .forms import TodoForm


# Create your views here.
def home(request):
    task1 = Task.objects.all()
    if request.method == "POST":
        name = request.POST.get('task', ' ')
        priority = request.POST.get('priority', ' ')
        date = request.POST.get('date', ' ')
        task = Task(name=name, priority=priority, date=date)
        task.save()

    return render(request, 'home.html', {'tasks': task1})


def delete(request, taskid):
    task = Task.objects.get(id=taskid)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    return render(request, 'delete.html')


def update(request, id):
    task = Task.objects.get(id=id)
    fm = TodoForm(request.POST or None, instance=task)
    if fm.is_valid():
        fm.save()
        return redirect('/')

    return render(request, 'edit.html', {'f': fm, 'task': task})
