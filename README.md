# Intro

This applications showcases the core functionality of GraphQl using Nameko and SQLAlchemy. 

## Getting Started

To run the application make sure you have `docker` and `docker-compose` installed then follow 
the steps below

* Run `docker-compose up` to start the service and wait for the app to start
* Go to your favorite GraphQL client and connect to http://localhost:5000/graphql and start writing queries

## Queries

Below are sample queries you can run.
```graphql
query getAllShips{
  allShip{
    edges{
      node{
        name
      }
    }
  }
}
```

```graphql
query crewDetails {
  allCrew(last: 10) {
    pageInfo {
      hasNextPage
      hasPreviousPage
      endCursor
      startCursor
    }
    edges {
      node {
        name
        ship {
          name
        }
        race {
          name
        }
        rank {
          name
        }
      }
      cursor
    }
  }
}
```

```graphql
{
  shipCrew(ship: "enterprise"){
    name,
    ship{
      name
    }
    rank{
      name
    }
    race {
      name
    }
  }
}
```
```graphql
query search{
  search(q: "c") {
    ... on Crew {
      name
    }
    ... on Race {
      name
    }
    ... on Rank {
      name
    }
    ... on Ship {
      name
    }
  }
}
```

## Mutations 
Below are some sample mutations
```graphql
mutation{
  addShip(shipData: {name: "U.S.S. Shenzhou"}){
    ship{
      name
      dateAdded
    }
  }
}
```

```graphql
mutation {
  addCrew(
    crewData: {
      name: "Philippa Georgiou"
      ship: "U.S.S. Shenzhou"
      rank: "Captain"
      race: "Human"
    }
  ) {
    name
    ship
    rank
    race
  }
}
```

```graphql
mutation {
  addRace(raceData: { name: "Bojorian" }) {
    race {
      name
    }
  }
}
```