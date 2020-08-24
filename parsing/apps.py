# -*- coding: utf-8
from django.apps import AppConfig


class ParsingConfig(AppConfig):
    name = 'parsing'

    def ready(self):
        import parsing.signals # pylint: disable=unused-import,import-outside-toplevel
