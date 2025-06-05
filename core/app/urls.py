from django.urls import path
from .views import (
    index,
    UploadImageView,
    ResizeImageView,
    MetaDataView,
    ListImagesView,
    DeleteImageView,
)

urlpatterns = [
    path("", index, name="index"),
    path("upload/", UploadImageView.as_view(), name="upload-image"),
    path("images/<str:filename>", ResizeImageView.as_view(), name="get-resized-image"),
    path("metadata/<str:filename>", MetaDataView.as_view(), name="get-meta-data"),
    path("images/", ListImagesView.as_view(), name="list-images"),
    path(
        "images/delete/<str:filename>", DeleteImageView.as_view(), name="delete-image"
    ),
]


# serve media files during development
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
