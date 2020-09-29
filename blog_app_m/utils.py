from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import BaseFormSet


from django.views.generic import View

from .models import *

class ObjectDetailMixin():
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj})

class ObjectCreateMixin(LoginRequiredMixin):

    model_form = None
    template = None

    def get(self,request):
        form = self.model_form()
        return render(request,self.template,context={'form':form})

    def post(self, request):
        bound_form = self.model_form(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.author = self.request.user
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template,context={'form':bound_form})

class ObjectUpdateMixin(LoginRequiredMixin,BaseFormSet):
    model = None
    model_form = None
    template = None


    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        instance = bound_form.save(commit=False)
        author = instance.author
        if self.request.user != author:
             return self.handle_no_permission()
        return render(request, self.template, context={'form': bound_form,self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST,instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form':bound_form, self.model.__name__.lower(): obj})

class ObjectDeleteMixin(LoginRequiredMixin):
    model = None
    model_form = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)

        bound_form = self.model_form(instance=obj)
        instance = bound_form.save(commit=False)
        author = instance.author
        if self.request.user != author:
            return self.handle_no_permission()

        return render(request, self.template, context={self.model.__name__.lower():obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))
