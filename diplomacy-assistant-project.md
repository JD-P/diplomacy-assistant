Diplomacy Move Assistant:
=========================

The diplomacy move assistant is a program that helps you play diplomacy, calculates 
optimal moves given a set of moves that the player expects other players to take, points out 

Map Description Format:
-----------------------

The map is described as a set of regions with properties without geographic 
connection, and then as the regions that border every sea region and every inland
region.

The rationale for this is that the minimal representation of a map depends on 
several properties of provinces in Diplomacy:

1. There are no one-way relationships between regions. That is, if you can move 
to a region A from a region B you can move to B from A.

2. A region that is coastal or a coast by definition borders a sea.

3. There are no isolated regions in a sane diplomacy board. Every region must in 
theory be linked to every other region. (Not directly, but by network.) We may 
call this the principle of isolation.

4. For any set of regions R, if every region in R borders every other region in R 
they're all connected. We may call such a construction a *collection*.

We can imagine every relation between two borders as a pair such as Washington -> Oregon 
in a map of the United States. The pairs between every border on the map are enough 
to calculate moves.

Because of the first property, we only have to actually specify half of the pair 
relations that comprise the map. For example, from Washington -> Oregon we know
that Oregon -> Washington also holds. So we only need to specify one of these two
pairs to be able to expand out to have the entire map.

The second property means that if we know the borders of every sea, and we know 
the borders of every inland region then we necessarily know where the coasts are.
This is because coasts are defined by their *not* being an inland region or sea,
as a consequence if we know both of those we know which regions are coastal.

The principle of isolation holds even for maps where there are in fact strange 
isolated regions. And the reason for this is that if a region or even a set of
regions is totally isolated from the mainland then it can't effect the game.
In a diplomacy map with two seperate regions you have to fight over that don't
effect each other this would essentially be playing two games of diplomacy at once.

Finally the collection is a way of further shortening the amount of information 
you need to give about the board. If every region in a collection is connected 
with each other then you only have to specify the regions in the collection and 
the rest of their properties are defined.

Map Description Syntax:
-----------------------

There are three things you want to be able to define with the map description
syntax:

* Regions - The type of province associated with a given name/id number.

* Collections - An abstraction on borders that lets you use property four to reduce
                the amount of information you have to give to specify a map.

* Borders - A two way relation between two regions of the form Washington -> Oregon
            describing their borders.

Each of these are as follows:

Regions:
--------

r, [id number]:[region name], [region type]

r - A marker to say that this is a region statement.

[id number] - A unique id number that identifies the region, id numbers should be
              between one and zero