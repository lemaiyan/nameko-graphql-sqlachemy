# Intro

This applications showcases the core functionality of GraphQl using Nameko and SQLAlchemy. 

## Getting Started

To run the application make sure you have `docker` and `docker-compose` installed then follow 
the steps below

* Run `docker-compose up` to start the service and wait for the app to start
* Go to your favorite GraphQL client and connect to http://localhost:5000/graphql and start writing queries

## Queries
```graphql
{
  shipCrew(ship: "discovery"){
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