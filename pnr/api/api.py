# Scrapping API
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from utils.utils import get_model
from utils.scrapping_utils import PnrScrapping
from django_extensions.db.models import ActivatorModel
from pnr.api.serializer import PnrDetailSerializer, PnrSerializer
from utils.exceptions import PNRNotFound
from pnr.tasks import send_pnr_details

PnrDetail = get_model(app_name="pnr", model_name="PnrDetail")
PassengerDetail = get_model(app_name="pnr", model_name="PassengerDetail")


class PnrScrapper(APIView):
    def post(self, request):
        pnr_serializer = PnrSerializer(data=request.data)
        pnr_serializer.is_valid(raise_exception=True)
        try:
            # If PNR Exists in database return data from database
            pnr_details = PnrDetail.objects.get(
                pnr=pnr_serializer.validated_data["pnr"],
                status=ActivatorModel.ACTIVE_STATUS,
            )
            serializer = PnrDetailSerializer(pnr_details)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PnrDetail.DoesNotExist:
            # If PNR Not Exists Fetch PNR
            try:
                scrapper = PnrScrapping(pnr_serializer.validated_data["pnr"])
                data = scrapper()
                serializer = PnrDetailSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                send_pnr_details.delay(request.user.id, serializer.data["id"])
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except PNRNotFound as pnr_not_found:
                print(pnr_not_found)
                return Response(
                    {"message": str(pnr_not_found)}, status=status.HTTP_400_BAD_REQUEST
                )
        except PnrDetail.MultipleObjectsReturned:
            return Response(
                {"message": "Multiple PNR Found"}, status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError as ve:
            return Response({"message": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(
                {"message": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request):
        pnr_serializer = PnrSerializer(data=request.data)
        pnr_serializer.is_valid(raise_exception=True)
        try:
            obj = PnrDetail.objects.get(pnr=pnr_serializer.validated_data["pnr"])
            scrapper = PnrScrapping(pnr_serializer.validated_data["pnr"])
            data = scrapper()
            serializer = PnrDetailSerializer(obj, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            send_pnr_details.delay(request.user.id, serializer.data["id"])
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PnrDetail.DoesNotExist:
            return Response(
                {"message": "PNR Not Found"}, status=status.HTTP_404_NOT_FOUND
            )
        except PnrDetail.MultipleObjectsReturned:
            return Response(
                {"message": "Multiple PNR Found"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
