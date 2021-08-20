from django.shortcuts import render
from django.views.generic import (TemplateView, DetailView,ListView, CreateView,UpdateView,DeleteView,FormView)
from .models import Department, Subject, Lesson, Comment
from django.urls import reverse_lazy
from .forms import CommentForm,ReplyForm, LessonForm
from django.http import HttpResponseRedirect
from app_users.models import AboutUs,Contact



class DepartmentListView(ListView):
    context_object_name = 'departments'
    model = Department
    template_name = 'curriculum/department_list_view.html'

    def get_context_data(self, **kwargs):
        objAbout = AboutUs.objects.all()[0]
        objContact = Contact.objects.all()
        context = super().get_context_data(**kwargs)
        context['aboutus'] = objAbout
        context['contactus'] = objContact
        return context

class SubjectListView(DetailView):
    context_object_name = 'departments'
    model = Department
    template_name = 'curriculum/subject_list_view.html'

    def get_context_data(self, **kwargs):
        objAbout = AboutUs.objects.all()[0]
        objContact = Contact.objects.all()
        context = super().get_context_data(**kwargs)
        context['aboutus'] = objAbout
        context['contactus'] = objContact
        return context

class LessonListView(DetailView):
    context_object_name = 'subjects'
    model = Subject
    template_name = 'curriculum/lesson_list_view.html'

    def get_context_data(self, **kwargs):
        objAbout = AboutUs.objects.all()[0]
        objContact = Contact.objects.all()
        context = super().get_context_data(**kwargs)
        context['aboutus'] = objAbout
        context['contactus'] = objContact
        return context


class LessonDetailView(DetailView, FormView):
    context_object_name = 'lessons'
    model = Lesson
    template_name = 'curriculum/lesson_detail_view.html'
    form_class = CommentForm
    second_form_class = ReplyForm

    def get_context_data(self, **kwargs):
        objAbout = AboutUs.objects.all()[0]
        objContact = Contact.objects.all()
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        context['aboutus'] = objAbout
        context['contactus'] = objContact
        if 'form' not in context:
            context['form'] = self.form_class(request=self.request)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(request=self.request)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.get_form_class()
            form_name = 'form'
        else:
            form_class = self.second_form_class
            form_name = 'form2'

        form = self.get_form(form_class)
       
        if form_name=='form' and form.is_valid():
            return self.form_valid(form)
        elif form_name=='form2' and form.is_valid():
            return self.form2_valid(form)


    def get_success_url(self):
        self.object = self.get_object()
        department = self.object.Department
        subject = self.object.subject
        return reverse_lazy('curriculum:lesson_detail',kwargs={'department':department.slug,'subject':subject.slug,'slug':self.object.slug})
   
    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.lesson_name = self.object.comments.name
        fm.lesson_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

    def form2_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get('comment.id')
        fm.save()
        return HttpResponseRedirect(self.get_success_url())


class LessonCreateView(CreateView):
    form_class = LessonForm
    context_object_name = 'subject'
    model= Subject
    template_name = 'curriculum/lesson_create.html'

    def get_context_data(self, **kwargs):
        objAbout = AboutUs.objects.all()[0]
        objContact = Contact.objects.all()
        context = super(LessonCreateView, self).get_context_data(**kwargs)
        context['aboutus'] = objAbout
        context['contactus'] = objContact
        return context

    def get_success_url(self):
        objAbout = AboutUs.objects.all()[0]
        objContact = Contact.objects.all()
        self.object = self.get_object()
        department = self.object.department
        return reverse_lazy('curriculum:lesson_list',kwargs={'department':department.slug,'slug':self.object.slug})


    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.Department = self.object.department
        fm.subject = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

class LessonUpdateView(UpdateView):
    fields = ('name','position','video','ppt','Notes')
    model= Lesson
    template_name = 'curriculum/lesson_update.html'
    context_object_name = 'lessons'

    def get_context_data(self, **kwargs):
        objAbout = AboutUs.objects.all()[0]
        objContact = Contact.objects.all()
        context = super().get_context_data(**kwargs)
        context['aboutus'] = objAbout
        context['contactus'] = objContact
        return context

class LessonDeleteView(DeleteView):
    model= Lesson
    context_object_name = 'lessons'
    template_name = 'curriculum/lesson_delete.html'

    def get_context_data(self, **kwargs):
        objAbout = AboutUs.objects.all()[0]
        objContact = Contact.objects.all()
        context = super(LessonDeleteView, self).get_context_data(**kwargs)
        context['aboutus'] = objAbout
        context['contactus'] = objContact
        return context

    def get_success_url(self):
        objAbout = AboutUs.objects.all()[0]
        objContact = Contact.objects.all()
        department = self.object.Department
        subject = self.object.subject
        return reverse_lazy('curriculum:lesson_list',kwargs={'department':department.slug,'slug':subject.slug})
