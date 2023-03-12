from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from loan.api import router


api = NinjaAPI()
api.add_router("/", router)

urlpatterns = [
    path('admin/', admin.site.urls),

    path("api/", api.urls),
]