from models import Ship as ShipModel
from models import Rank as RankModel
from models import Race as RaceModel
from models import Crew as CrewModel

import graphene
import logging
from graphene import relay
from sqlalchemy import func
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from database import db_session


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


class ShipInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class RaceInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class RankInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class CrewInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    rank = graphene.String(required=True)
    race = graphene.String(required=True)
    ship = graphene.String(required=True)


class AddShipMutation(graphene.Mutation):
    class Arguments:
        ship_data = ShipInput(required=True)

    ship = graphene.Field(Ship)

    @staticmethod
    def mutate(root, info, ship_data=None):
        ship = ShipModel(name=ship_data.name)
        db_session.add(ship)
        db_session.commit()

        return AddShipMutation(ship=ship)


class AddRankMutation(graphene.Mutation):
    class Arguments:
        rank_data = RankInput(required=True)

    rank = graphene.Field(Rank)

    @staticmethod
    def mutate(root, info, rank_data=None):
        rank = RankModel(name=rank_data.name)
        db_session.add(rank)
        db_session.commit()

        return AddRankMutation(rank=rank)


class AddRaceMutation(graphene.Mutation):
    class Arguments:
        race_data = RaceInput(required=True)

    race = graphene.Field(Race)

    @staticmethod
    def mutate(root, info, race_data=None):
        race = RaceModel(name=race_data.name)
        db_session.add(race)
        db_session.commit()

        return AddRaceMutation(race=race)


class CrewOutput(graphene.ObjectType):
    name = graphene.String()
    rank = graphene.String()
    race = graphene.String()
    ship = graphene.String()


class AddCrewMutation(graphene.Mutation):
    class Arguments:
        crew_data = CrewInput(required=True)

    Output = CrewOutput

    @staticmethod
    def mutate(root, info, crew_data=None):
        logging.info(f'add-crew-mutation {crew_data}')
        rank = Rank.get_query(info).filter(func.lower(RankModel.name) == func.lower(crew_data.rank)).first()
        logging.info(f'rank {rank.name}')
        race = Race.get_query(info).filter(func.lower(RaceModel.name) == func.lower(crew_data.race)).first()
        logging.info(f'race {race.name}')
        ship = Ship.get_query(info).filter(ShipModel.name.ilike(f'%{crew_data.ship}%')).first()
        logging.info(f'ship {ship}')
        crew = CrewModel(name=crew_data.ship)
        logging.info(f'crew {crew.name}')
        output = CrewOutput()
        output.name = crew.name
        if rank:
            crew.rank = rank
            output.rank = rank.name
        if race:
            crew.race = race
            output.race = race.name
        if ship:
            crew.ship = ship
            output.ship = ship.name
        db_session.add(crew)
        db_session.commit()

        return output


class Mutations(graphene.ObjectType):
    add_ship = AddShipMutation.Field()
    add_rank = AddRankMutation.Field()
    add_race = AddRaceMutation.Field()
    add_crew = AddCrewMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
