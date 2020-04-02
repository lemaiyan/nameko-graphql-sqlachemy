from models import Ship as ShipModel
from models import Rank as RankModel
from models import Race as RaceModel
from models import Crew as CrewModel

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType


class Crew(SQLAlchemyObjectType):
    class Meta:
        model = CrewModel

class Ship(SQLAlchemyObjectType):
    class Meta:
        model = ShipModel
        interfaces = (graphene.relay.Node,)

    def get_node(cls, info, id):
        query = Ship.get_query(info)
        return query.get(id)

class Rank(SQLAlchemyObjectType):
    class Meta:
        model = RankModel
        interfaces = (graphene.relay.Node,)

    def get_node(cls, info, id):
        query = Rank.get_query(info)
        return query.get(id)

class Race(SQLAlchemyObjectType):
    class Meta:
        model = RaceModel
        interfaces = (graphene.relay.Node,)

    def get_node(cls, info, id):
        query = Race.get_query(info)
        return query.get(id)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_crew = graphene.List(Crew)
    crew_count = graphene.Int()

    @staticmethod
    def resolve_all_crew(parent, info):
        query = Crew.get_query(info)
        return query.all()

    @staticmethod
    def resolve_crew_count(parent, info):
        query = Crew.get_query(info)
        return query.count()


schema = graphene.Schema(query=Query)
