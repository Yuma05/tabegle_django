from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response

from api.models import Place
from api.serializer import PlaceSerializer


class SearchPlace(generics.ListAPIView):
    serializer_class = PlaceSerializer

    def get_queryset(self):
        try:
            queryset = Place.objects.filter(
                Q(name__contains=self.request.query_params['q']) | Q(kana__contains=self.request.query_params['q'])
            )
        except Exception:
            raise Exception("Not found search keywords.")
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
        except Exception:
            return Response({"message": 'Not found search keywords.'})

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
