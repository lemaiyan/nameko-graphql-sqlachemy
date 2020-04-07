import structlog
from graphql_server import (default_format_error,
                            encode_execution_results, json_encode,
                            load_json_body, run_http_query)

from database import init_db
from schema import schema

logger = structlog.get_logger()


class App():
    def __init__(self):
        init_db()

    def query(self, request):
        logger.info("begin-query")
        data = self.parse_body(request)
        logger.info("query", request=request)
        execution_results, params = run_http_query(
            schema,
            'post',
            data)
        result, status_code = encode_execution_results(
            execution_results,
            format_error=default_format_error, is_batch=False, encode=json_encode)
        logger.info("query", result=result, status_code=status_code)
        logger.info("end-query")
        return result

    def parse_body(self, request):
        logger.info('start-parse-body')
        content_type = request.mimetype
        query = None
        if content_type == 'application/graphql':
            query = {'query': request.data.decode('utf8')}

        elif content_type == 'application/json':
            query = load_json_body(request.data.decode('utf8'))

        elif content_type in ('application/x-www-form-urlencoded', 'multipart/form-data'):
            query = request.form

        logger.info('parse-body', query=query, content_type=content_type)
        logger.info('end-parse-body')

        return query
