#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print ("unable to connect to %s database" % database_name)


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    cursor.execute("DELETE FROM matches;")
    cursor.execute("UPDATE standings SET wins=0, matches =0;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    cursor.execute("DELETE FROM standings;")
    cursor.execute("DELETE FROM players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    query = "SELECT count(*) FROM players;"
    cursor.execute(query)
    data = cursor.fetchone()
    db.close()
    return data[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    cursor.execute("INSERT INTO players (name) values (%s)", (name,))
    db.commit()
    cursor.execute("SELECT * from players ORDER BY id DESC LIMIT 1;")
    data = cursor.fetchone()
    cursor.execute("""INSERT INTO standings (player_id, name, wins, matches)
        values (%s, %s, 0, 0);""", (data[1], data[0]))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, cursor = connect()
    cursor.execute("SELECT * FROM standings;")
    standings = [(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()]
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # update match table
    # update standings
    db, cursor = connect()
    cursor = db.cursor()
    cursor.execute("""INSERT INTO matches(winner, loser)
        values (%d, %d);""" % (winner, loser))
    db.commit()

    # update winner
    cursor.execute("""SELECT * FROM standings WHERE
            player_id=%d LIMIT 1;""" % winner)
    data = cursor.fetchone()
    updatedWins = int(data[2]) + 1
    updatedMatches = int(data[3]) + 1
    cursor.execute("""UPDATE standings SET  wins=%d, matches=%d
        WHERE player_id=%d;""" % (updatedWins, updatedMatches, winner))
    db.commit()

    # update loser
    cursor.execute("""SELECT * FROM standings
        WHERE player_id=%d LIMIT 1;""" % loser)
    data = cursor.fetchone()
    updatedMatches = int(data[3]) + 1
    cursor.execute("""UPDATE standings SET matches=%d
        WHERE player_id=%d;""" % (updatedMatches, loser))
    db.commit()

    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db, cursor = connect()
    cursor.execute("SELECT * FROM standings ORDER BY wins;")
    data = cursor.fetchall()
    # matchNum is the number of matches
    matchNum = len(data)/2
    matchList = []
    for x in range(0, matchNum):
        # step through players in twos
        y = x*2
        matchList.append((data[y][0], data[y][1], data[y+1][0], data[y+1][1]))
    db.close()
    return matchList
