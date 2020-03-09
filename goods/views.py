from rest_framework import viewsets

from goods import (models, serializers)


class GoodViewSet(viewsets.ModelViewSet):
    queryset = models.Good.objects.all()
    serializer_class = serializers.GoodSerializer
