"""
Views for the track APIs
"""
from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Track,
    Book,
    Task,
)
from track import serializers
from task import serializers as taskserializers
from book import serializers as bookserializers


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'books',
                OpenApiTypes.STR,
                description='Comma separated list of book IDs to filter',
            ),
            OpenApiParameter(
                'tasks',
                OpenApiTypes.STR,
                description='Comma separated list of task IDs to filter',
            ),
        ]
    )
)


class TrackAllViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subject_major', 'subject_minor', 'target_test', 'target_grade']

    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return serializers.TrackDetailSerializer


class TrackViewSet(viewsets.ModelViewSet):
    """View for manage track APIs."""
    serializer_class = serializers.TrackDetailSerializer
    queryset = Track.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subject_major', 'subject_minor', 'target_test', 'target_grade']

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve tracks for authenticated user."""
        books = self.request.query_params.get('books')
        tasks = self.request.query_params.get('tasks')
        queryset = self.queryset
        if books:
            book_ids = self._params_to_ints(books)
            queryset = queryset.filter(books__id__in=book_ids)
        if tasks:
            task_ids = self._params_to_ints(tasks)
            queryset = queryset.filter(tasks__id__in=task_ids)

        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.TrackSerializer
        elif self.action == 'upload_image':
            return serializers.TrackImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new track."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to track."""
        track = self.get_object()
        serializer = self.get_serializer(track, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to recipes.',
            ),
        ]
    )
)
class BaseTrackAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(track__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('-track_name').distinct()


class TaskViewSet(BaseTrackAttrViewSet):
    """Manage tracks in the database."""
    serializer_class = taskserializers.TaskSerializer
    queryset = Task.objects.all()


class BookViewSet(BaseTrackAttrViewSet):
    """Manage books in the database."""
    serializer_class = bookserializers.BookSerializer
    queryset = Book.objects.all()
