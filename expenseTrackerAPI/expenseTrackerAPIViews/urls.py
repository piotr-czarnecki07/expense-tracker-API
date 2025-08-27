from expenseTrackerAPIViews.views import userViews, opreationViews
from django.urls import path

urlpatterns = [
    path('/user/signup', userViews.signup),
    path('/user/login', userViews.login),
    path('/user/remind', userViews.remindToken),
    path('/user/logout', userViews.logout),

    path('/operation/add', opreationViews.addExpense),
    path('/operation/delete', opreationViews.deleteExpenses),
    path('/operation/update', opreationViews.updateExpenses),
    path('/operation/get', opreationViews.getExpenses)
]