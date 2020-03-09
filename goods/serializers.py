from rest_framework import serializers

from goods import models


class GoodSerializer(serializers.ModelSerializer):
    # category = serializers.StringRelatedField()
    # brand = serializers.StringRelatedField()
    # care_type = serializers.StringRelatedField()

    class Meta:
        model = models.Good
        fields = '__all__'
