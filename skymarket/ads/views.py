from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, viewsets

from ads.models import Ad, Comment

from ads.serializers import AdSerializer, AdDetailSerializer, CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

from ads.filters import AdFilter


class AdPagination(pagination.PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 4


class AdViewSet(viewsets.ModelViewSet):
    default_queryset = Ad.objects.all()
    queryset = Ad.objects.all()
    default_serializer_class = AdDetailSerializer
    pagination_class = AdPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = AdFilter

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
    queryset = Comment.objects.all().select_related('ad')
    serializer_class = CommentSerializer

    def get_queryset(self, *args, **kwargs):
        ad_id = self.kwargs.get('ad_pk')
        ad = get_object_or_404(Ad, pk=ad_id)

        return self.queryset.filter(ad=ad)


    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(author=self.request.user, ad_id=self.kwargs.get('ad_pk'))


