from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from candidate.forms import CandidateProfileForm
from django.views.generic import TemplateView,CreateView,DetailView,ListView,UpdateView
from candidate.models import CandidateProfile
from employer.models import Jobs,Applications
from users.decorators import signin_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from candidate.filters import JobFilter
from users.models import User
from users.forms import UserRegistrationForm
from django.core.cache import cache
from django.core.paginator import Paginator

# admin;anj pass:anj
@method_decorator(signin_required,name='dispatch')
class CandidateHomeView(TemplateView):
    template_name = "cand-home.html"

    def get(self,request,*args,**kwargs):
        filter=JobFilter(request.GET,queryset=Jobs.objects.all())
        jobs_paginator=Paginator(filter.qs,2)
        page=jobs_paginator.get_page(1)
        return render(request,"cand-home.html",{"filter":filter})
@method_decorator(signin_required,name='dispatch')
class CandidateProfileCreateView(CreateView):
    model=CandidateProfile
    form_class = CandidateProfileForm
    template_name = "cand-profile.html"
    success_url = reverse_lazy("cand-home")

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

@method_decorator(signin_required,name='dispatch')
class CandidateProfileDetailView(TemplateView):
    template_name = "cand-myprofile.html"

class CandidateProfileUpdateView(UpdateView):
    model = CandidateProfile
    form_class = CandidateProfileForm
    template_name = "cand-profileedit.html"
    success_url = reverse_lazy("cand-home")
    pk_url_kwarg = "id"
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

@method_decorator(signin_required,name='dispatch')
class CandidateJobDetailView(DetailView):
    template_name = "cand-detailjob.html"
    model=Jobs
    context_object_name = "job"
    pk_url_kwarg = "id"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        qs=Applications.objects.filter(applicant=self.request.user,job=self.object)
        context["status"]=qs
        return context

@signin_required
def logoutview(request,*args,**kwargs):
    logout(request)
    cache.clear()
    return redirect("cand-home")

@signin_required
def applynow(request,*args,**kwargs):
    job_id=kwargs.get('id')
    job=Jobs.objects.get(id=job_id)
    applicant=request.user
    Applications.objects.create(applicant=applicant,job=job)
    return redirect("cand-home")

@method_decorator(signin_required,name='dispatch')
class CandidateAllJobsView(ListView):
    template_name = "cand-list.html"
    model = Jobs
    context_object_name = "jobs"
    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     qs = Jobs.objects.all()
    #     context["jobs"] = qs
    #     return context
    def get(self,request,*args,**kwargs):
        qs=Jobs.objects.all()
        job_paginator=Paginator(qs,2)
        page_num=request.GET.get('page')
        page=job_paginator.get_page(page_num)
        return render(request,"cand-list.html",{"page":page})
@method_decorator(signin_required,name='dispatch')
class AppliedView(ListView):
    model = Applications
    template_name = "cand-appliedjobs.html"
    context_object_name = "applied"

    def get_queryset(self):
        return Applications.objects.filter(applicant=self.request.user)

@method_decorator(signin_required,name='dispatch')
class JobNotification(ListView):
    model = Applications
    template_name = "accepted-jobs.html"
    context_object_name = "application"

    def get_queryset(self):
        return Applications.objects.filter(applicant=self.request.user,status='accepted')

@method_decorator(signin_required,name='dispatch')
class PasswordReset(UpdateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "reset-password.html"
    success_url = reverse_lazy("cand-home")
    pk_url_kwarg = "id"

@signin_required
def removeprofile(request,*args,**kwargs):
    profile=kwargs.get("id")
    CandidateProfile.objects.filter(id=profile).delete()
    return redirect("e-home")