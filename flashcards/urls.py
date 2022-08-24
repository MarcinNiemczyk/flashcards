from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.explore, name='explore'),
    path('library', views.library, name='library'),
    path('add', views.add_collection, name='add collection'),
    path('edit/<int:collection_id>', views.edit_collection, name='edit'),
    path('collection/<int:collection_id>', views.collection_details, name='collection')
]

# Serving files uploaded by a user during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
