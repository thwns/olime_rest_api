"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import (
    Track,
    Book,
    Profile,
    Task,
)

from book import serializers as bookserializers
from task import serializers as taskserializers
from profiles import serializers as profileserializers

'''class BookSerializer(serializers.ModelSerializer):
    """Serializer for tag_subject_majors."""

    class Meta:
        model = Book
        fields = ['id', 'name']
        read_only_fields = ['id']


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for tag_subject_minors."""

    class Meta:
        model = Profile
        fields = ['id', 'name']
        read_only_fields = ['id']


class Tag_Target_TestSerializer(serializers.ModelSerializer):
    """Serializer for tag_target_tests."""

    class Meta:
        model = Tag_Target_Test
        fields = ['id', 'name']
        read_only_fields = ['id']


class Tag_Target_GradeSerializer(serializers.ModelSerializer):
    """Serializer for tag_target_grades."""

    class Meta:
        model = Tag_Target_Grade
        fields = ['id', 'name']
        read_only_fields = ['id']'''


class TrackSerializer(serializers.ModelSerializer):
    """Serializer for tracks."""
    profile = profileserializers.ProfileDetailSerializer(read_only=True)
    book = bookserializers.BookDetailSerializer(required=False)
    task = taskserializers.TaskDetailSerializer(required=False)

    class Meta:
        model = Track
        fields = [
            'id', 'profile', 'subject_major', 'subject_minor', 'target_test',
            'target_grade', 'track_name', 'book', 'link',
            'followers_num', 'rating_avg', 'task', 'image', 'published_date',
        ]
        read_only_fields = ['id']


class TrackDetailSerializer(TrackSerializer):
    """Serializer for track detail view."""

    class Meta(TrackSerializer.Meta):
        fields = TrackSerializer.Meta.fields + ['description']

    def _get_or_create_book(self, books, track):
        """Handle getting or creating books as needed."""
        auth_user = self.context['request'].user
        for book in books:
            book_obj, created = Book.objects.get_or_create(
                user=auth_user,
                **book,
            )
            track.books.add(book_obj)

    def _get_or_create_tasks(self, tasks, track):
        """Handle getting or creating tasks as needed."""
        auth_user = self.context['request'].user
        for task in tasks:
            task, created = Task.objects.get_or_create(
                user=auth_user,
                **task,
            )
            track.tasks.add(task_obj)

    def create(self, validated_data):
        """Create a recipe."""
        books = validated_data.pop('books', [])
        tasks = validated_data.pop('tasks', [])
        track = Track.objects.create(**validated_data)
        self._get_or_create_books(books, track)
        self._get_or_create_tasks(tasks, track)

        return track


    def update(self, instance, validated_data):
        """Update recipe."""
        books = validated_data.pop('books', None)
        tasks = validated_data.pop('tasks', None)
        if books is not None:
            instance.books.clear()
            self._get_or_create_books(books, instance)
        if tasks is not None:
            instance.tasks.clear()
            self._get_or_create_tasks(tasks, instance)


        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class TrackmageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to tracks."""

    class Meta:
        model = Track
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}
