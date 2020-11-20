from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response

from api.models import Category
from api.serializer import CategorySerializer


class SearchCategory(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        try:
            queryset = Category.objects.filter(
                Q(name__contains=self.request.query_params['q']) | Q(kana__contains=self.request.query_params['q'])
            )
        except:
            raise Exception("Not found search keywords.")
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
        except:
            return Response({"message": 'Not found search keywords.'})

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
