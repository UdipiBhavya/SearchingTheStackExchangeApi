from django.contrib import admin
from django.urls import path
from .import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('search/questions',views.search_questions,name="search_questions"),
    path('',views.display,name="display")
]