"""
Serializers for book APIs
"""
from rest_framework import serializers

from core.models import Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer for books."""

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'sub_title', 'author', 'image_url',
            'isbn', 'publisher', 'published_date',
        ]
        read_only_fields = ['id']


class BookDetailSerializer(BookSerializer):
    """Serializer for Book detail view."""

    class Meta(BookSerializer.Meta):
        fields = BookSerializer.Meta.fields + ['image_url']
