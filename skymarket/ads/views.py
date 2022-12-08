from rest_framework import pagination, viewsets

from ads.models import Ad

from ads.serializers import AdSerializer, AdDetailSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class AdPagination(pagination.PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 4


class AdViewSet(viewsets.ModelViewSet):
    default_queryset = Ad.objects.all()
    queryset = Ad.objects.all()
    default_serializer_class = AdDetailSerializer
    pagination_class = AdPagination

    serializers = {
        'list': AdSerializer,

    }

    querysets = {
        'retrieve': Ad.objects.select_related('author')
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        return self.querysets.get(self.action, self.default_queryset)

    @action(detail=False, url_path='me')
    def my_ads(self, request):
        ads = Ad.objects.filter(author=request.user)
        page = self.paginate_queryset(ads)
        if page is not None:
            serializer = self.get_serializer(ads, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(ads, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)





class CommentViewSet(viewsets.ModelViewSet):
    pass
