from rest_framework import serializers

class DocumentUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class QuerySerializer(serializers.Serializer):
    query = serializers.CharField()
