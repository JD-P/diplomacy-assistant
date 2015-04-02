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

Each of these are as follows, but first some notes on how to read the syntax
descriptions:

Tokens that are unadorned such as 'r,' should be typed as is. 

Tokens that are surrounded in square brackets are a stand in for a more general
type of value or variable, usually described by the phrase in the brackets.

Ellipsis imply that a token or pattern can be repeated indefinitely.

An asterick to the *right* of an object means that token is optional, and within
context that anything which might come after that token may also be optional.

Regions:
--------

r, [id number]:[region name], [region type]:[nickname]

r - A marker to say that this is a region statement.

[id number] - A unique id number that identifies the region, id numbers should be
              between one and zero

[region name] - The string representing the name of the region. Every character 
between the colon and the comma will be represented in the name here exactly as
typed, so be careful about ones use of spaces and remember to use capitalization.

[region type] - An integer representing one of the region types, see the section
"Region Types" in this document for more information. 

[nickname] - A unique nickname representing this country in future statements.

Collections:
------------

c, [comma seperated common bases]:[completion:*completion...], [completion:*completion...]...

(As a note, all of that goes onto one line even if the description 

c - A marker to say that this is a collection statement.

[common bases] - A comma seperated set of region name/nick/id's representing the common base 
of the collection.

[completion] - Comma seperated set of region name/nick/id's that when combined with the base regions 
forms a collection.

:* - An optional argument (only the colon is typed) in which you can specify a
base on top of the initial base already specified. What this means is that if 
multiple collections overlap across certain common regions you can define those
overlaps and then list every element of the collection only once.

Example: c, [Sil]:[Mun: Boh, Ber], [Pru: Ber, War], [Gal: Boh, War]

A description of the 'Silesia' province and surrounding territories in the classic 
diplomacy map.

We may be interested in knowing the information efficiency of this approach.
Instead of measuring in bits I will measure in the ratio of regions typed to
borders represented. The calculations are as follows:

Imagine a set of regions [A, B]. A and B would have the following border closure:

A -> B

B -> A

Giving us a total of two. If we imagine another set [A, B, C] its closure would be:

A -> B, C

B -> A, C

C -> A, B

For six border pairs. The rule by which we have gone from six to two is that we
both added one to every items border relations in the set *and* added another 
item. That is, from two sets of one to three sets of two. In general:

The number of items n multiplied by n minus one will give us the borders 
represented by a set of regions which all border each other.

What this means for our format is that to get the number of borders represented
by a collection statement we do:

For each base case, go to the furthest base case in each set and multiply the 
depth of the base by the depth minus one, then for each non-base region multiply
the depth of the base case it belongs to plus one by the depth of the base case
to which it belongs. 

As an illustration with the Silesia example above:

We have three depth-two bases with two non-base regions each.

(2 * 1) * 3 = 6

(3 * 2) * 3 = 18

Now, it's important to note at this point that there is overlap between these two
values. What we actually want is the *unique* number of values produced by each.

Let's go back to the simplest case: A:[B:C]

We have a depth of two that produces two sets of one. When we add our third
region C we get two *new* relations for A and B, and then two new relations
for region C. If we subtracted 2 from 6 to get 4 we would have the correct
number of border relations produced by each.

An alternative method of calculating this is the depth of the base to which
the region belongs plus one new relation for every base, or the depth of the
base multiplied by two for every non-base region belonging to the base. 

To move back to our earlier example, our real number of border relations for
each would then be:

(2 * 1) * 3 = 6

(2 * 2) * 3 = 12

6 - 18 = 12, since we found this result by two different methods we can be fairly
sure it is correct and that our final total is 18.

We get this representation by naming ten regions, since the theoretical minimum 
description is half, or in this case nine regions we are fairly close to the limit
of what is possible in terms of how few regions you can describe of the regions you
*must* describe.
 
Borders:
--------

b, [region name/nick/id]:[region name/nick/id]

b - A marker to say that this is a border statement.

[region name/nick/id] - The name/nick/id of a region that shares a border with the other region,
the order of the relation does not matter since it applies in both directions.

Example: b, [0]:[1]