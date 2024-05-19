from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView,CreateView,ListView,DetailView,UpdateView
from employer.forms import EmployerProfileForm,JobForm
from employer.models import EmployerProfile,Jobs,Applications
from users.decorators import signin_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.contrib import messages
from employer.filters import PostedJobFilter


# user:employer pass:Password@123
@method_decorator(signin_required,name='dispatch')
class EmployerHomeView(TemplateView):
    template_name = "emp-home.html"

    def get(self,request,*args,**kwargs):
        filter=PostedJobFilter(request.GET,queryset=Jobs.objects.all())
        return render(request,"emp-home.html",{"filter":filter})

@method_decorator(signin_required,name='dispatch')
class EmployerProfileCreateView(CreateView):
    model=EmployerProfile
    form_class = EmployerProfileForm
    template_name = "emp-profile.html"
    success_url = reverse_lazy("e-home")


    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,'Job has been posted successfully')
        return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     form=EmployerProfileForm(request.POST,files=request.FILES)
    #     if form.is_valid():
    #        profile= form.save(commit=False)
    #        profile.user=request.user
    #        profile.save()
    #        print("profile created")
    #        return redirect("e-home")
    #     else:
    #         return render(request,self.template_name,{"form":form})


@method_decorator(signin_required,name='dispatch')
class EMployeeProfileDetailView(TemplateView):
    template_name = "emp-myprofile.html"

@method_decorator(signin_required,name='dispatch')
class EmployerProfileUpdateView(UpdateView):
    model=EmployerProfile
    form_class = EmployerProfileForm
    template_name = "emp-profileupdate.html"
    success_url = reverse_lazy("e-home")
    pk_url_kwarg = "id"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

@method_decorator(signin_required,name='dispatch')
class JobCreateView(CreateView):
    model=Jobs
    form_class =JobForm
    template_name = "emp-postjob.html"
    success_url =reverse_lazy("e-home")

    def form_valid(self, form):
        form.instance.posted_by=self.request.user
        return super().form_valid(form)


@method_decorator(signin_required,name='dispatch')
class EmployerJobListView(ListView):
    model = Jobs
    context_object_name = "jobs"
    template_name = "emp-joblist.html"
    # paginate_by = 2

    def get_queryset(self):
        return Jobs.objects.filter(posted_by=self.request.user).order_by('-created_date')



@method_decorator(signin_required,name='dispatch')
class JobDetailView(DetailView):
    model=Jobs
    template_name = "emp-jobdetail.html"
    context_object_name = "job"
    pk_url_kwarg = "id"

@method_decorator(signin_required,name='dispatch')
class JobUpdateView(UpdateView):
    model = Jobs
    template_name = "emp-jobupdate.html"
    form_class = JobForm
    success_url = reverse_lazy("emp-listjob")
    pk_url_kwarg = "id"

@signin_required
def logout(request,*args,**kwargs):
    logout(request)
    return redirect("signin")

@method_decorator(signin_required,name='dispatch')
class AppliedCandidatesView(ListView):
    model = Applications
    template_name = "applied-cand.html"
    context_object_name = "appliedcand"
    def get_queryset(self):
        return Applications.objects.filter(job=self.kwargs.get("id"))

@method_decorator(signin_required,name='dispatch')
class AppliedCandidatesDetailedView(ListView):
    model = Applications
    template_name = "applied-cand-detailed.html"
    context_object_name = "detailcand"
    pk_url_kwarg = "id"

@signin_required
def reject_application(request,*args,**kwargs):
    app_id=kwargs.get('id')
    qs=Applications.objects.get(id=app_id)
    qs.status="rejected"
    qs.save()
    return redirect("applied-cand")

@signin_required
def accept_application(request,*args,**kwargs):
    app_id=kwargs.get('id')
    qs=Applications.objects.get(id=app_id)
    qs.status="accepted"
    qs.save()
    send_mail(
        'Job Notification',
        'You have been accepted',
        'mealdrin007@gmail.com',
        ['aveenaseb@gmail.com'],
        fail_silently=False,
    )
    return redirect("emp-listjob")


@signin_required
def removeprofile(request,*args,**kwargs):
    profile=kwargs.get("id")
    EmployerProfile.objects.filter(id=profile).delete()
    return redirect("e-home")