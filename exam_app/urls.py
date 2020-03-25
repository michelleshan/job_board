from django.urls import path
from . import views

urlpatterns=[
    path('',views.index),
    path('createUser',views.create_user),
    path('logIn',views.login),
    path('dashboard',views.dashboard),
    path('destroy',views.destroy),
    path('addJob',views.add_job),
    path('createJob',views.create_job),
    path('view/<int:id>',views.view_job),
    path('addToMyJobs/<int:id>',views.add_to_my_jobs),
    path('removeFromMyJobs/<int:id>',views.remove_from_my_jobs),
    path('edit/<int:id>',views.edit_job),
    path('updateJob/<int:id>',views.update_job),
    path('cancelJob/<int:id>',views.cancel_job)
]