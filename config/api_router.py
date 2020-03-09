from rest_framework.routers import DefaultRouter, SimpleRouter
from django.conf import settings
from coreapi.users.api.views import UserViewSet

from goods import views


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("good", views.GoodViewSet)

app_name = "api"
urlpatterns = router.urls
