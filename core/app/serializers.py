from .models import CustomImage, ImageMetaData
from rest_framework import serializers


class ImageMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageMetaData
        fields = "__all__"


class CustomImageSerializers(serializers.ModelSerializer):

    meta_data = ImageMetaDataSerializer(read_only=True)  # nested!

    class Meta:
        model = CustomImage
        fields = "__all__"  # it takes all fields in the model

    def validate_image(
        self, image
    ):  # django rest framework triggers this def automatically because it starts with validate_fieldname

        # if you upload images like .HEIC which is not suported by django, the code will not be able to reach here it will give a built in error (which is provided by django ImageField)

        valid_types = ["image/jpeg"]  # example required type
        if (
            image.content_type not in valid_types
        ):  # content_type returns like 'image/jpeg' etc.
            raise serializers.ValidationError(
                "Unsupported image type, only JPEG is allowed."
            )

        # size validation
        max_size = 10 * 1024 * 1024
        if image.size > max_size:
            raise serializers.ValidationError(
                "Image file too large, Maximum size allowed is 10MB."
            )

        return image
