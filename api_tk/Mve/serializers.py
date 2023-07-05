from rest_framework import serializers
from Mve.models import MvModel


class MvSerializer(serializers.ModelSerializer):
    class Meta:
        model = MvModel
        fields = '__all__'

    def validate(self, attrs):
        title = attrs.get('title')
        director = attrs.get('director')
        genre= attrs.get('genre')
        release_date = attrs.get('release_date')
        if not title:
            raise serializers.ValidationError("Title is required.")
        if len(title) > 20:
            raise serializers.ValidationError("Title cannot exceed 20 characters.")

        # if not director:
        #     raise serializers.ValidationError("Director is required.")
        # if len(director) > 100:
        #     raise serializers.ValidationError("Director name cannot exceed 100 characters.")

        return attrs