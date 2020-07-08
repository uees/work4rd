from rest_framework import routers

from apps.account import views as account_views
from apps.basedata import views as basedata_views

router = routers.DefaultRouter()
router.register(r'account/users', account_views.UserViewSet)
router.register(r'account/groups', account_views.GroupViewSet)
router.register(r'basedata/material-categories', basedata_views.MaterialCategoryViewSet)
router.register(r'basedata/materials', basedata_views.MaterialViewSet)
