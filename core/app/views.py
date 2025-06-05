from django.utils import timezone
from django.http import HttpResponse

from rest_framework.views import APIView
from .serializers import CustomImageSerializers
from .models import CustomImage, ImageMetaData

from rest_framework.response import Response
from rest_framework import status

import os
from django.conf import settings
from django.http import FileResponse, Http404
from PIL import Image
from io import BytesIO

from django.core.files.base import ContentFile


# test
def index(request):
    return HttpResponse("Success")


class UploadImageView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomImageSerializers(data=request.data)
        if serializer.is_valid():
            custom_image_obj = serializer.save()

            uploaded_file = request.FILES["image"]

            mime_type = uploaded_file.content_type
            file_name = uploaded_file.name

            # create metadata object
            metadata = ImageMetaData.objects.create(
                og_image_width=custom_image_obj.image.width,
                og_image_height=custom_image_obj.image.height,
                upload_time=timezone.now(),
                MIME_type=mime_type,
                og_file_name=file_name,
            )
            custom_image_obj.meta_data = metadata
            custom_image_obj.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResizeImageView(APIView):
    def get(self, request, filename):
        image_path = os.path.join(
            settings.MEDIA_ROOT, "original", filename
        )  # media/original/<filename>

        if not os.path.exists(image_path):
            raise Http404("Image not found.")

        try:

            custom_image = CustomImage.objects.get(image=f"original/{filename}")

            if (
                custom_image.resized_image
            ):  # if the image has been already resized for once it wont resize again
                return FileResponse(
                    open(custom_image.resized_image.path, "rb"),
                    content_type="image/jpeg",
                )

            with Image.open(
                image_path
            ) as img:  # open the image file from disk using its file path

                img = img.resize((224, 224))

                # --- to display image ---
                buffer = BytesIO()
                img.save(buffer, format="JPEG")
                buffer.seek(0)
                # ------------------------

                resized_filename = f"resized-{filename}"
                custom_image.resized_image.save(
                    resized_filename, ContentFile(buffer.read()), save=True
                )  # saving to the resized image field of same CustomImage object

                # ---------- update some part of metadata -------------
                custom_image.meta_data.resized_image_width = (
                    custom_image.resized_image.width
                )
                custom_image.meta_data.resized_image_height = (
                    custom_image.resized_image.height
                )
                custom_image.meta_data.resized_file_name = resized_filename

                custom_image.meta_data.save()
                # ---------------------------------------------------------

                buffer.seek(0)
                return FileResponse(buffer, content_type="image/jpeg")

        except Exception as e:
            return HttpResponse(f"Error processing image: {str(e)}", status=400)


class MetaDataView(APIView):  # return the meta data of the image
    def get(self, request, filename):
        image_path = os.path.join(
            settings.MEDIA_ROOT, "original", filename
        )  # media/original/<filename>

        if not os.path.exists(image_path):
            raise Http404("Image not found.")

        try:

            custom_image = CustomImage.objects.get(image=f"original/{filename}")

            if custom_image.meta_data is None:
                return Response(
                    {"error": "Metadata not available for this image."}, status=404
                )

            data = {
                "original_width": custom_image.meta_data.og_image_width,
                "original_height": custom_image.meta_data.og_image_height,
                "resized_width": custom_image.meta_data.resized_image_width,
                "resized_height": custom_image.meta_data.resized_image_height,
                "upload_time": custom_image.meta_data.upload_time.isoformat(),
                "mime_type": custom_image.meta_data.MIME_type,
                "original_filename": custom_image.meta_data.og_file_name,
                "resized_filename": custom_image.meta_data.resized_file_name,
            }

            return Response(data, status=200)

        except Exception as e:
            return HttpResponse(f"Error processing image: {str(e)}", status=400)


# ------- BONUS ENDPOINTS -----------

# /images?resized=true OR /images?filename=<filename> OR /images?filename=do<filename>g&resized=false OR /images


class ListImagesView(APIView):  # list all images or filter
    def get(self, request):
        queryset = CustomImage.objects.all()  # fetch all objects

        filename = request.query_params.get("filename")  # filters
        resized = request.query_params.get("resized")

        if filename:
            queryset = queryset.filter(image__icontains=filename)

        if resized == "true":
            queryset = queryset.filter(resized_image__isnull=False)
        elif resized == "false":
            queryset = queryset.filter(resized_image__isnull=True)

        serializer = CustomImageSerializers(queryset, many=True)
        return Response(serializer.data)


# request: curl -X DELETE http://127.0.0.1:8000/images/delete/<file_name>
class DeleteImageView(APIView):  # delete the image
    def delete(self, request, filename):
        try:
            image_obj = CustomImage.objects.get(image=f"original/{filename}")

            # delete original file
            if image_obj.image and os.path.exists(image_obj.image.path):
                os.remove(image_obj.image.path)

            # delete resized file if it exists
            if image_obj.resized_image and os.path.exists(image_obj.resized_image.path):
                os.remove(image_obj.resized_image.path)

            # delete the image object itself
            image_obj.delete()

            return Response(
                {"message": f"{filename} and its metadata deleted."},
                status=status.HTTP_200_OK,
            )

        except CustomImage.DoesNotExist:
            raise Http404("Image not found.")
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
