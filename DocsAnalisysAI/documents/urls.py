from django.urls import path
from .views import UploadDocumentView, SearchDocumentView

urlpatterns = [
    path("upload/", UploadDocumentView.as_view(), name="upload-document"),
    path("search/", SearchDocumentView.as_view(), name="search-document"),
]
