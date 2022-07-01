from django.conf.urls import url, include

from hub.routes import RPRouter

from ask_chip.views import AskChipViewSet, SearchHandlerViewSet

router = RPRouter()
router.register(r'ask_chip', AskChipViewSet)
router.register(r'search_handler', SearchHandlerViewSet)

urlpatterns = [
   url(r'^api/', include(router.urls)),
]
