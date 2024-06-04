from rest_framework import serializers
from .models import Project, Task, Comment
from datetime import datetime

from pytz import timezone

class ProjectSerializerModel(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def validate_name(self, value):
        if 'Daniel' in value:
            raise serializers.ValidationError('Name cannot contain Daniel')
        return value

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        Project(**validated_data).save()
        return self.data

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.init_date = validated_data.get('init_date', instance.init_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.save()
        return instance

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def validate_content(self, value):
        # Add your validation logic here. For example, check if the content is not offensive.
        if 'offensive_word' in value:
            raise serializers.ValidationError('Content cannot contain offensive words')
        return value


class ProjectSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=60)
    init_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField()

    def validate_name(self, value):
        if 'Daniel' in value:
            raise serializers.ValidationError('Name cannot contain Daniel')
        return value


    def validate(self, attrs):

        return super().validate(attrs)

    def create(self, validated_data):

        Project(**validated_data).save()
        return self.data