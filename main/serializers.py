from django.utils.html import strip_tags
from django.utils import timezone
from rest_framework import serializers

from main.models import Project
from main.models import Experience

class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "tech_stack",
            "url_link", "image",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_tech_stack(self, value):
        return strip_tags(value)

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())

class ExperienceSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    is_current = serializers.SerializerMethodField()

    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    category_display = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = Experience
        fields = [
            "id", "title", "description", "category", "category_display" , "thumbnail", "started_at", "ended_at", "duration", "is_current", "star_count", "is_starred", "starred_by_names"
        ]

        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_category(self, value):
        if value not in dict(Experience.EXPERIENCE_CHOICES):
            raise serializers.ValidationError("Invalid Category")
        return value

    def validate_thumbnail(self, value):
        return strip_tags(value)

    def get_is_current(self, obj):
        return obj.ended_at is None

    def get_duration(self, obj):
        if not obj.started_at:
            return 0
        end = obj.ended_at or timezone.now().date()
        months = (end.year - obj.started_at.year) * 12 + (end.month - obj.started_at.month)
        return max(months, 0)

    def validate(self, data):
        started = data.get("started_at")
        ended = data.get("ended_at")
        if started and ended and ended < started:
            raise serializers.ValidationError("ended_at cannot be before started_at")
        return data

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())
