from django.urls import path
from employer import views
from candidate.views import PasswordReset

urlpatterns=[
    path("emphome",views.EmployerHomeView.as_view(),name="e-home"),
    path("profiles/add",views.EmployerProfileCreateView.as_view(),name="emp-profile"),
    path('profile/update/<int:id>',views.EmployerProfileUpdateView.as_view(),name="emp-updateprofile"),
    path("profiles/details",views.EMployeeProfileDetailView.as_view(),name="emp-detail"),
    path("jobs/add",views.JobCreateView.as_view(),name="emp-addjob"),
    path("jobs/all",views.EmployerJobListView.as_view(),name="emp-listjob"),
    path("jobs/detail/<int:id>",views.JobDetailView.as_view(),name="emp-jobdetail"),
    path("jobs/update/<int:id>",views.JobUpdateView.as_view(),name="emp-jobupdate"),
    path("applied/<int:id>",views.AppliedCandidatesView.as_view(),name="applied-cand"),
    path("applied/details/<int:id>",views.AppliedCandidatesDetailedView.as_view(),name="cand-details"),
    path("status/reject/<int:id>",views.reject_application,name="rejected"),
    path("status/accept/<int:id>",views.accept_application,name="accepted"),
    path("profile/remove<int:id>",views.removeprofile,name="profileremove"),
    path("password/reset",PasswordReset.as_view(),name="passreset"),
]