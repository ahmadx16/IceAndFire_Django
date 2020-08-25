from rest_framework import serializers


class ExternalBookSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    isbn = serializers.CharField(max_length=50)
    authors = serializers.ListField(child=serializers.CharField(max_length=50))
    numberOfPages = serializers.IntegerField()
    publisher = serializers.CharField(max_length=50)
    country = serializers.CharField(max_length=50)
    released = serializers.DateTimeField(format="%Y-%m-%d")

    def to_representation(self, instance):
        """Convert `username` to lowercase."""
        ret = super().to_representation(instance)
        ret['number_of_pages'] = ret.pop('numberOfPages')
        ret['release_date'] = ret.pop('released')
        
        return ret


