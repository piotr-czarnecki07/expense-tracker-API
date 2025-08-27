from django.urls import path, include

urlpatterns = [
    path('', include('expenseTrackerAPIViews.urls')),
]
