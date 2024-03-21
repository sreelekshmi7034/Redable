from Tools.scripts.make_ctype import method
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Task
from .forms import TodoForm
from django.views.generic import ListView, UpdateView, DeleteView
from django.views.generic import DetailView


# Create your views here.

class TaskListView(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'tasks'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'details.html'
    context_objects_name = 'task'


class TaskUpdateView(UpdateView):
    model = Task
    template_name = "updates.html"
    context_object_name = "task"
    fields = ('name', 'priority', 'date')

    def get_success_url(self):
        return reverse_lazy('cbvdetails', kwargs={'pk': self.object.id})


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')


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
