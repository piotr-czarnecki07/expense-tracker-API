from expenseTrackerAPI.expenseTrackerAPIViews.views import userViews, opreationViews
from django.urls import path

urlpatterns = [
    path('/user/signup', userViews.signup),
    path('/user/login', userViews.login),
    path('/user/remind', userViews.remindToken),
    path('/user/logout', userViews.logout),

    path('/operation/add', opreationViews.signup),
    path('/operation/delete', opreationViews.signup),
    path('/operation/update', opreationViews.signup),
    path('/operation/get', opreationViews.signup)
]