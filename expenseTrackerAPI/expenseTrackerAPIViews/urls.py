from expenseTrackerAPIViews.views import userViews, opreationViews
from django.urls import path

urlpatterns = [
    path('user/signup/', userViews.signup),
    path('user/login/', userViews.login),
    path('user/remind/', userViews.remind_token),
    path('user/logout/', userViews.logout),

    path('operation/add/', opreationViews.add_expense),
    path('operation/delete/', opreationViews.delete_expenses),
    path('operation/update/', opreationViews.update_expenses),
    path('operation/get/', opreationViews.get_expenses)
]
