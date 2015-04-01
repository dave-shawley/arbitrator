"""
Arbitrator
==========

"""
version_info = (1, 0, 0)
__version__ = '.'.join(str(v) for v in version_info)


from ietfparse.algorithms import select_content_type
from ietfparse.errors import NoMatch
from ietfparse.headers import parse_content_type, parse_http_accept_header


class MediaTypeMixin(object):

    default_media_type = None
    """Media type to use when nothing else matches the Accept header."""

    media_types = None
    """Mapping between media types and their serializer."""

    supported = set()
    """Set of supported IETF Accept headers."""

    def initialize(self, *args, **kwargs):
        if MediaTypeMixin.media_types is None:
            types = kwargs.pop('media_types', {})
            supported = {parse_content_type(mime) for mime in types}
            MediaTypeMixin.media_types = media_types
            MediaTypeMixin.supported = supported

        if MediaTypeMixin.default_media_type is None:
            MediaTypeMixin.default_media_type = kwargs.pop(
                'default_media_type')

        self.__parsed_content_type = None
        self.__parsed_accept_headers = None

        super(MediaTypeMixin, self).initialize(*args, **kwargs)

    @property
    def content_type_header(self):
        """Returns the Content-Type header for the time being."""
        if self.__parsed_content_type is None:
            header = self.request.headers.get(
                'Content-Type', self.default_media_type)

            if header is None:
                raise web.HTTPError(415)

            self.__parsed_content_type = parse_content_type(header)

        return self.__parsed_content_type

    @property
    def accept_headers(self):
        """Returns all Accept headers."""
        if self.__parsed_accept_headers:
            header = self.request.headers.get(
                'Accept', self.default_media_type)

            if header is None:
                raise web.HTTPError(406)

            self.__parsed_accept_headers = parse_http_accept_header(header)

        return self.__parsed_accept_headers

    def load_payload(self, **kwargs):
        """Deserializes ``payload`` with the provided Content-Type header.

        If the request ``payload`` cannot be deserialized we will return
        a 400.  If there no support registered for the Content-Type header
        then we will raise a 415.

        :param dict payload:
            The Python dictionary containing the data.

        :param dict kwargs:
            Additional keyword args passed to the serializer.

        :returns: Dictionary containing the request data.

        """
        header = str(self.content_type_header)
        try:
            return self.media_types[header].loads(self.request.content)
        except ValueError:
            reason = 'Unable to load payload with {0} header'.format(header)
            raise web.HTTPError(400, reason=reason)

    def dump_payload(self, payload, **kwargs):
        """Serializes ``payload`` with the proper accept type.

        Returns a tuple consisting of the media type selected for
        serialization and the serialized data.  If the ``payload`` cannot
        be serialized we will return a 400.  If there no support registered
        for the accept header the we will raise a 406.

        :param dict payload:
            The dictionary containing the data to be serialized.

        :param dict kwargs:
            Additional keyword args passed to the serializer.

        :returns:
            Tuple containing the selected Accept header used and
            the serialized data matching the selected header.

        """
        accept = self.accept_headers

        try:
            requested, selected = select_content_type(self.supported, accept)
            selected = str(selected)
            serializer = self.media_types[selected].dumps
            return selected, serializer(payload, **kwargs)
        except NoMatch:
            raise web.HTTPError(406, )
        except ValueError:
            reason = 'Unable to dump payload with {0} header'.format(selected)
            raise web.HTTPError(400, reason=reason)
