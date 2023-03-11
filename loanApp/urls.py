
from django.urls import path
from loan.api import router

urlpatterns = [
    path('api/', router.urls),
]
