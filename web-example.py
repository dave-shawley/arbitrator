import datetime
import json
import logging

from arbitrator.tornado import ArbitratedApplication, ArbitratedHandler
from tornado import ioloop, web
import yaml


class YamlHandler(object):
    @staticmethod
    def dumps(data):
        return yaml.safe_dump(data, default_flow_style=False)
    @staticmethod
    def loads(data_str):
        return yaml.safe_load(data_str)


class DateHandler(ArbitratedHandler, web.RequestHandler):
    def get(self, tz):
        if tz == 'utc':
            now = datetime.datetime.utcnow()
        elif tz == 'local':
            now = datetime.datetime.now()
        else:
            raise web.HTTPError(400)

        rep = {
            'month': now.month,
            'day': now.day,
            'year': now.year,
        }
        self.write(self.encode_response(rep))


def make_app():
    return ArbitratedApplication(
        handlers=[
            web.url(r'/now/(utc|local)', DateHandler),
        ],
        content_handlers=[
            ('application/json', json),
            ('application/yaml', YamlHandler),
        ],
        debug=True,
    )


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)1.1s - %(name)s: %(message)s.')
    app = make_app()
    app.listen(8000)
    ioloop.IOLoop.current().start()
