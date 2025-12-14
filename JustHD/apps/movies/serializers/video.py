from rest_framework import serializers
from apps.movies.models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'quality', 'size', 'duration', 'video_file')
        read_only_fields = ('id',)