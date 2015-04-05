# Diplomacy assistant: A tool to help one plan and play a game of diplomacy.

import argparse 

import json

import string

def main():
    """Parse arguments and then run the rest of the program according to them."""
    parser = argparse.ArgumentParser()
    parser.add_argument("regions", type=argparse.FileType('r'), 
                        help="The filepath to read a list of regions comprising" \ 
                             " the map from.")
    parser.add_argument("borders", type=argparse.FileType('r'), 
                        help="The filepath to read a list of borders describing" \ 
                             " the relationships between regions from.") 
    parser.add_argument("--check", action="store_true", 
                        help="Check the given map for consistency and print test" \ 
                             " results.")
    arguments = parser.parse_args()
    regions = json.load(arguments.regions)
    borders = json.load(arguments.borders)
    if arguments.check:
        mapmaker.consistency_checker(regions, borders)
        return 1
    else:
        

class MapMaker():
    """Import a set of region descriptions to make a map."""
    def make_map(cls, description):
        board = {}
        for region in description:
            region_id = region[0]
            region_values = region[1]
            board = cls.add_region(cls, board, region_id, region_values[0], 
                                region_values[1], region_values[2], region_values[3], region_values[4])
        return board

    def add_region(cls, board, region_id, name, nickname, region_type):
        region = {}
        region['name'] = name
        region['nick'] = nickname
        region['type'] = region_type
        board[region_id] = region
        return board
    
    def input_map(cls):
        """Interface to put a map into memory as a series of statements and
        translate into an internal representation."""
        regions = {}
        borders = {}
        history = []
        print("Start inserting statements now.")
        while history[-2:] is not ["\n","\n"]:
            statement = input(">")
            tokens = cls.parse_statement(statement)
            if tokens:
                statement_type = tokens[0]
            else:
                continue
            if statement_type = "r":

    def parse_statement(cls, statement):
        """Parse a statement given in map descripton or game description format
        and return its internal representation."""
        split = statement.split(",", 1)
        statement_type = split[0]
        universal = split[1]
        if statement_type == "r":
            try:
                region_id = int(universal.split(":")[0])
            except ValueError:
                print("Invalid Region id")
                return False
            metadata = universal.split(":")[1]
            elements = metadata.split(",")
            try:
                name = elements[0].strip(string.whitespace)
            except IndexError:
                print("Invalid region name.")
                return False
            try:
                region_type = elements[1].strip(string.whitespace)
            except IndexError:
            nickname = elements[2].strip(string.whitespace)
            return
    def consistency_checker(cls, regions, borders):
        """Takes a dict of regions and a dict of borders, checking for anomalies.

        Keyword Arguments:
        regions: A dictionary with region id's for keys containing lists with the 
                 metadata describing the region.
        borders: A dictionary with region id's for keys and the id's of regions 
                 which border it in a list as its value.
        """
        print("Test One: Duplicate Checking:")
        region_components = set()
        for region_id in regions:
            region_name = regions[region_id]['name']
            region_nick = regions[region_id]['nick']            
            if region_id in region_components:
                raise ValueError("Region id " + str(region_id) + 
                                 " is duplicated in the list of regions.")
            elif region_name in region_components:
                raise ValueError("Region name " + str(regions[region_id]['name']) 
                                 + " is duplicated in the list of regions.")
            elif region_nick in region_components:
                raise ValueError("Region nick " + str(regions[region_id]['nick'])
                                 + " is duplicated in the list of regions.")
            else:
                region_components.add(region_id)
                region_components.add(region_name)
                region_components.add(region_nick)
        print("Test Two: Spell Checking and Name Consistency:")
        region_names = [region[0] for region in list(regions.values())]
        for border in borders:
            names = borders[border][:]
            if border in names:
                raise ValueError("Region " + border + " lists itself as a bordering region.")
            names.append(border)
            for name in names:
                if name not in region_names:
                    raise ValueError("Region name " + "'" + name + "'" + " in " 
                                     + border + " is in conflict with its " \
                                     "counterpart in the list of regions.")
        print("Test Three: Data Consistency in Regions:")
        """This test follows a set of rules to determine if any of the countries are 
        malformed within the context of the data structures used to represent regions.
        This test does *not* determine if a regions information is inaccurate in its
        values, but if the region as written is allowed to exist at all.

        There are 2 rules that this test uses to detect errors of this kind, they are:
        0. If a region has no elements, a length other than three it is invalid.
        1. If a region does not have a type value between zero and six it is invalid.        
        """
        for region in regions:
            region = regions[region]
            if len(region) is not 3:
                try:
                    raise ValueError("Region " + region['name'] + " has only its name " \
                                      "as its elements or is missing a nickname" \
                                      " or only has a nickname.")
                except ValueError:
                    raise ValueError("A given region has no elements.") 
            elif region['type'] is in (3,6):
                print(region['name'] + " is a coast.")
            elif region['type'] is in (1,2,4,5):
                print(region['name'] + " is inland or coastal.")
            elif region['type'] is 0:
                print(region['name'] + " is a sea.")
            else:
                print("Something strange happened with " + region['name'] + ".")
        """This test tries to verify the integrity of region information through the
        bordering regions of seas supplied as part of the map description. Everything
        that borders a sea is necessarily a coastal region or itself a sea. Everything
        that claims to be a coastal region necessarily borders a sea. There are no one
        way relationships in diplomacy so we can generate pairs of relationships that
        are two way for every sea and every coastal region. 

        What this means in practice is that if a region is coastal but no seas claim 
        to border it, then either the region is not really coastal, it has not been 
        included in the borders of the sea in which it should be included, or the sea 
        which includes it as a border has not been added to the map. If a sea claims 
        to border a region and it is not coastal, then either the region description
        is correct and it has been improperly added as a border or the region is coastal
        and has been improperly described.

        In either case it is left up to a human as to how to correct the error.
        """
        def is_sea_coastal_coast(region):
            """Verifies that a given region is a sea, coast or coastal region."""
            if region['type'] is not in (1,4):
                return True
            else:
                return False

        def is_sea(region):
            """Verifies that a given region is a sea."""
            if region['type'] is 0:
                return True
            else:
                return False
        for sea in borders:
            
            if is_sea(regions[sea]) is False:
                raise ValueError(str(regions[sea]) + " is listed as a sea with " \
                                     "borders when it is not coded as a sea in " \
                                     "regions.")
            sea_borders = borders[sea]
            for region in sea_borders:
                region = regions[region]
                if is_sea_coastal_coast(region) is False:
                    raise ValueError(str(region) + " is in the borders of " \
                                         + borders[sea] + "when it is not coded as" \
                                         "a sea, coast, or coastal region.")
                else:
                    continue
        print("Testing finished, in so far as this program can discern the map is " \
               "valid, but that does not actually guaruntee the map is correct.")
        return True
                            

class Diplomacy():
    """Represents a diplomacy game and implements features such as resolving moves
    and trying to figure out the optimal set of moves for a given player this turn."""
    
    def __init__(self, game_description):
        
        players = 

    def resolve(self, board, game_state, orders):
        """Resolve given a board and a game state with orders for that board."""

