from rest_framework import routers

from api.views import DeckViewSet

router = routers.DefaultRouter()
router.register(r"decks", DeckViewSet, basename="deck")

urlpatterns = router.urls
