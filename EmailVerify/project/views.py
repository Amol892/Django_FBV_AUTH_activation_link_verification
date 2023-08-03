from django.shortcuts import redirect, render
from django.views import View
from .models import Project_details
from .forms import ProjectForm
from django.contrib.auth.mixins import LoginRequiredMixin

class Project_view(LoginRequiredMixin,View):
    
    template_name='project/project.html'
    
    def get(self,request):
        form = ProjectForm()
        context={'form':form}
        return render(request,self.template_name,context)
    
    def post(self,request):
        form =ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_url')
        else:
            form=ProjectForm()
            context={'form':form}
            return render(request,self.template_name,context)
        
class Home_view(LoginRequiredMixin,View):
    template_name = 'project/home.html'
    
    def get(self,request):
        obj=Project_details.objects.all()
        context = {'object':obj}
        return render(request,self.template_name,context)