![alt text](https://github.com/andrewtdunn/tournamentPlanner/blob/master/passedTest.png "screenshot")

#tournamentPlanner

A Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.

The game tournament uses the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible.

##to create database

Within psql:

```bash


vagrant@trusty32: vagrant => \i tournament.sql
CREATE DATABASE
You are now connected to database "tournament" as user "vagrant".
CREATE TABLE
CREATE TABLE
CREATE VIEW
tournament=>


```
This will initialize the tournament database and create players, matches, and standings tables

##to run tests

within main directory:

```bash



$> python tournament_test.py


```


