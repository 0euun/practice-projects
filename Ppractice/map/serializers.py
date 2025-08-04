from rest_framework import serializers

class LibrarySerializer(serializers.Serializer):
    title = serializers.CharField()
    link = serializers.CharField(allow_null=True, required=False)
    category = serializers.CharField(allow_null=True, required=False)
    description = serializers.CharField(allow_null=True, required=False)
    telephone = serializers.CharField(allow_null=True, required=False)
    address = serializers.CharField()
    roadAddress = serializers.CharField(allow_null=True, required=False)
    mapx = serializers.CharField()
    mapy = serializers.CharField()
    map_url = serializers.CharField()
    open_time = serializers.CharField()
    close_day = serializers.CharField()
    facility = serializers.CharField()
