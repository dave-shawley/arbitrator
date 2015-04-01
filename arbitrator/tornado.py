import logging

from ietfparse import algorithms, errors, headers
from tornado import web


_logger = logging.getLogger(__name__)


class ArbitratedApplication(web.Application):

    def __init__(self, *args, **kwargs):
        self._default_content_type = kwargs.pop('default_content_type',
                                                'application/octet-stream')
        self._supported_mime_types = set()
        self._handlers = {}
        for content_type, handler in kwargs.pop('content_handlers', []):
            parsed = headers.parse_content_type(content_type)
            self._supported_mime_types.add(parsed)
            self._handlers[parsed] = handler

        super(ArbitratedApplication, self).__init__(*args, **kwargs)

    def decode_request(self, request):
        content_type = headers.parse_http_accept_header(
            request.headers.get('Content-Type', self._default_content_type))
        try:
            selected, _ = algorithms.select_content_type(
                content_type, self._supported_mime_types)
            handler = self._handlers[selected]
        except errors.NoMatch:
            raise web.HTTPError(415)
        return handler.loads(request.body)

    def encode_response(self, request, response_body):
        accept_target = request.headers.get(
            'Accept', self._default_content_type)
        _logger.debug('determining response type, '
                      'client wants %s and I can produce %s',
                      accept_target, self._supported_mime_types)
        acceptable = headers.parse_http_accept_header(accept_target)
        try:
            selected, _ = algorithms.select_content_type(
                acceptable, self._supported_mime_types)
        except errors.NoMatch:
            selected = self._default_content_type

        _logger.debug('selected content type %s', selected)
        try:
            handler = self._handlers[selected]
        except KeyError:
            raise web.HTTPError(406)
        _logger.debug('dumping with %r', handler)
        return str(selected), handler.dumps(response_body)


class ArbitratedHandler(object):

    def decode_request(self):
        return self.application.decode_request(self.request)

    def encode_response(self, response_body):
        content_type, body = self.application.encode_response(
            self.request, response_body)
        self.set_header('Content-Type', content_type)
        return body
