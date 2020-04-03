from models import Ship as ShipModel
from models import Rank as RankModel
from models import Race as RaceModel
from models import Crew as CrewModel

import graphene
from graphene import relay
from sqlalchemy import func
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType


class Crew(SQLAlchemyObjectType):
    class Meta:
        model = CrewModel
        interfaces = (graphene.relay.Node,)

    def get_node(cls, info, id):
        query = Crew.get_query(info)
        return query.get(id)


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


class SearchResult(graphene.Union):
    class Meta:
        types = (Crew, Ship, Rank, Race)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_crew = SQLAlchemyConnectionField(Crew)
    all_ship = SQLAlchemyConnectionField(Ship)
    all_rank = SQLAlchemyConnectionField(Rank)
    all_races = SQLAlchemyConnectionField(Race)
    in_race = graphene.List(Crew, race=graphene.String())
    in_rank = graphene.List(Crew, rank=graphene.String())
    ship_crew = graphene.List(Crew, ship=graphene.String())
    search = graphene.List(SearchResult, q=graphene.String())

    @staticmethod
    def resolve_in_race(parent, info, **args):
        race = args.get('race').lower()
        query = Crew.get_query(info).join(RaceModel, CrewModel.rank).filter(
            func.lower(RaceModel.name) == func.lower(race))
        return query.all()

    @staticmethod
    def resolve_in_rank(parent, info, **args):
        rank = args.get('rank').lower()
        query = Crew.get_query(info).join(RankModel, CrewModel.rank).filter(
            RankModel.name.ilike(f'%{rank}%'))
        return query.all()

    @staticmethod
    def resolve_ship_crew(parent, info, **args):
        ship = args.get('ship').lower()
        query = Crew.get_query(info).join(ShipModel, CrewModel.ship).filter(
            ShipModel.name.ilike(f'%{ship}%'))
        return query.all()

    @staticmethod
    def resolve_search(parent, info, **args):
        q = args.get('q').lower()
        rank_query = Rank.get_query(info)
        race_query = Race.get_query(info)
        ship_query = Ship.get_query(info)
        crew_query = Crew.get_query(info)

        rank = rank_query.filter(RankModel.name.contains(q)).all()
        race = race_query.filter(RaceModel.name.contains(q)).all()
        ship = ship_query.filter(ShipModel.name.contains(q)).all()
        crew = crew_query.filter(CrewModel.name.contains(q)).all()

        return rank + race + ship + crew


schema = graphene.Schema(query=Query)
