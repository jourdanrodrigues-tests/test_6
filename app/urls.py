from rest_framework.routers import SimpleRouter

from app.views import ChocolatePreferenceViewSet, OrderViewSet

router = SimpleRouter()
router.register('chocolate_preference', ChocolatePreferenceViewSet)
router.register('orders', OrderViewSet)
