from rest_framework import renderers


class DataTablesRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        print
        print('######################')
        print(data)
        print('############')
        ret = super(DataTablesRenderer, self).render(data, accepted_media_type, renderer_context)
        return ret
