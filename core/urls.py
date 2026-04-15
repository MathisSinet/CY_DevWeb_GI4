from django.urls import path
from accounts.views import *
from accounts.utils import upgradeLevel

urlpatterns = [
    path("upgrade/<str:level>/", upgradeLevel, name="upgrade_level")
]
