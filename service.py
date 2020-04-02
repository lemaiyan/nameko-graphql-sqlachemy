from app import App
from nameko.web.handlers import http


class StarTrekService:
    name = 'Star Trek'

    @http('POST', '/graphql')
    def query(self, request):
        return App().query(request)
