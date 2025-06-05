from django.db import models


class ImageMetaData(models.Model):
    og_image_width = models.IntegerField()
    og_image_height = models.IntegerField()

    resized_image_width = models.IntegerField(blank=True, null=True)
    resized_image_height = models.IntegerField(blank=True, null=True)

    upload_time = models.DateTimeField()

    MIME_type = models.CharField(max_length=31)

    og_file_name = models.CharField(max_length=255)
    resized_file_name = models.CharField(max_length=255, blank=True, null=True)


class CustomImage(models.Model):
    image = models.ImageField(upload_to="original/")
    resized_image = models.ImageField(upload_to="resized/", null=True, blank=True)
    # This field for resized version of original image. Since we do not have to resize each image this field can be null and blank.
    # if we resize the image this field will be used.
    meta_data = models.OneToOneField(
        ImageMetaData, on_delete=models.CASCADE, null=True, blank=True
    )
    # OneToOneField: each custom image object has exactly one image meta data object
    # models.CASCADE: if the custom image object is deleted, image meta data also will be deleted
