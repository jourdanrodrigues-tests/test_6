from rest_framework.routers import SimpleRouter

from app.views import ChocolatePreferenceViewSet

router = SimpleRouter()
router.register('chocolate_preference', ChocolatePreferenceViewSet)
