from rest_framework import serializers

class MoveSerializer(serializers.Serializer):
    source = serializers.ListField(child=serializers.IntegerField())
    dest = serializers.ListField(child=serializers.IntegerField())

