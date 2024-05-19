from django.urls import path
from candidate import views

urlpatterns=[
    path("home",views.CandidateHomeView.as_view(),name="cand-home"),
    path("profiles/add",views.CandidateProfileCreateView.as_view(),name="cand-addprofile"),
    path("jobs/details/<int:id>",views.CandidateJobDetailView.as_view(),name="cand-detailjob"),
    path("profile/details",views.CandidateProfileDetailView.as_view(),name="cand-detail"),
    path("profile/edit/<int:id>",views.CandidateProfileUpdateView.as_view(),name="cand-editprofile"),
    path("accounts/logout",views.logoutview,name="signout"),
    path("application/add/<int:id>",views.applynow,name="apply-now"),
    path("all/jobs",views.CandidateAllJobsView.as_view(),name="cand-list"),
    path("jobs/applied",views.AppliedView.as_view(),name="cand-applied"),
    path("jobs/accepted",views.JobNotification.as_view(),name='accepted'),
    path("password/reset/<int:id>",views.PasswordReset.as_view(),name="passreset"),
    path("profile/remove<int:id>",views.removeprofile,name="profileremove"),
]