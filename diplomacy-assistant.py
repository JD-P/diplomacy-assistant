# Diplomacy assistant: A tool to help one plan and play a game of diplomacy.

import argparse 

import json

def main():
    """Parse arguments and then run the rest of the program according to them."""
    parser = argparse.ArgumentParser()
    parser.add_argument("regions", type=argparse.FileType('r'), 
                        help="The filepath to read a list of regions comprising\ 
                              the map from.")
    parser.add_argument("borders", type=argparse.FileType('r'), 
                        help="The filepath to read a list of borders describing\ 
                              the relationships between regions from.") 
    parser.add_argument("--check", action="store_true", 
                        help="Check the given map for consistency and print test\ 
                              results.")
    arguments = parser.parse_args()
    regions = json.load(arguments.regions)
    borders = json.load(arguments.borders)
    if arguments.check:
        mapmaker.consistency_checker(regions, borders)
        return 1
    else:
        

class mapmaker():
    """Import a set of region descriptions to make a map."""
    # TODO: Define a text file format to import such descriptions from.
    def make_map(description):
        board = {}
        for region in description:
            region_id = region[0]
            region_values = region[1]
            board = mapmaker.add_region(board, region_id, region_values[0], 
                                region_values[1], region_values[2], region_values[3], region_values[4])
        return board

    def add_region(board, region_id, name, land, sea, supply, neighbors):
        region = {}
        region['name'] = name
        region['land'] = land
        if sea:
            region['sea'] = sea
        if supply:
            region['supply'] = supply
        region['neighbors'] = neighbors
        board[region_id] = region
        return board
    
    def consistency_checker(regions, borders):
        """Takes a list of regions and a list of borders, checking for anomalies.

        Keyword Arguments:
        regions: A list containing a series of lists describing regions on the board.
        borders: A list of dictionaries with the name of a region as their key and the regions which border it in a list as its value.
        """
        print("Test One: Duplicate Checking:")
        region_ids = set()
        for region_id in regions:
            if region_id in region_ids:
                raise ValueError("Region " + str(regions[region_id][0]) + " is duplicated in the list of regions.")
            else:
                region_ids.add(region)
                
        print("Test Two: Spell Checking and Name Consistency:")
        region_names = [region[0] for region in list(regions.values())]
        for border in borders:
            names = borders[border][:]
            if border in names:
                raise ValueError("Region " + border + " lists itself as a bordering region.")
            names.append(border)
            for name in names:
                if name not in region_names:
                    raise ValueError("Region name " + "'" + name + "'" + " in " + border + " is in conflict with its counterpart in the list of regions.")
        print("Test Three: Data Consistency in Regions:")
        """This test follows a set of rules to determine if any of the countries are 
        malformed within the context of the data structures used to represent regions.
        This test does *not* determine if a regions information is inaccurate in its
        values, but if the region as written is allowed to exist at all.

        There are 6 rules that this test uses to detect errors of this kind, they are:
        0. If a region has no elements, a length of one or a length of over four it
        is invalid.
        1. If a region does not have 'coast' in the name and it has a truth value for
        anything after having 'land' set to false it is invalid.
        2. If a region has 'coast' in the name and any truth values after the first two
        it is invalid.
        3. If a region has a first truth value of true and two or less truth values 
        it is invalid.
        4. If a region has 'coast' in the name and land is set to 'true' it is invalid.
        5. If a region has 'coast' in the name and only one truth value after it is
        invalid.

        Valid regions have the following possible values:
        1. True, [True OR False], [True OR False]
        2. False
        3. If Coast is True (otherwise invalid): False, [True OR False] 
        
        There are fourteen possible combinations of three truth values if one can
        remove values to create subsets. Whether or not a name has 'coast' in it is 
        also a true or false value, but does not count as a 'truth value' for the rules
        above. Giving us thirty possible values. We can be sure that this set of rules 
        and recognizers is complete if it covers 30 unique cases and the empty set
        ('True False or None' is in fact ternary, 3^4 is 81 but there are 31 *unique*
        values :
        Values with an asterick (*) next to them are optional, we calculate them
        combinatorically as being ternary.

        Rule zero covers three cases: [*[T or F]], [[T OR F], [T OR F], [T OR F], 
        [T OR F], [T OR F]...]
        Rule one covers six cases: [F, F, [T OR F], *[T OR F]]
        Rule two covers eight cases: [T, [T OR F], [T OR F], [T OR F]] (Overlaps four with rule nine)
        Rule three covers three cases: [F, T, *[T OR F]]
        Rule four covers nine cases: [T, T, *[T OR F], *[T OR F]] (Overlaps two with itself.)
        Rule five covers two cases: [T, [T OR F]] (One overlap with rule four)
        The first valid region recognizer has four cases: [F, T, [T OR F], [T OR F]]
        The second valid region recognizer has one case: [F, F]
        The third valid region recognizer has two cases: [T, F, [T OR F]]
        (3 + 6 + 8 + 3 + 9 + 2 + 4 + 1 + 2) - (4 + 2 + 1) = 31

        One way that this could be shown to be an incorrect proof of covering all
        cases is if you can show that any of the cases covered by one rule or recognizer
        overlap with cases covered by another rule or recognizer, thus making them not
        unique. You can play with the tools I used to generate this proof under truth
        -expansion in the source files.
        """
        for region in regions:
            region = regions[region]
            if len(region) < 2 or len(region) > 4: # Rule zero
                try:
                    raise ValueError("Region " + region[0] + " has only its name as its elements.")
                except ValueError:
                    raise ValueError("A given region has no elements.") 
            elif 'coast' in region[0].lower(): 
                if len(region) > 3: # Rule two
                    raise ValueError("Length of coast " + region[0] + " is invalid.")
                elif region[1]: # Rule four
                    raise ValueError("Coast " + region[0] + " has a land value of 'true'")
                elif len(region) == 2: # Rule five, other cases covered by rule zero
                    raise ValueError("Coast " region[0] " only has one truth value as an element.")
            elif len(region) > 2: #Necessary to safely test rule one and set up rule three
                if region[1] is False: # Rule one
                    raise ValueError("Region " + region[0] + " has truth values" \
                                      " after having 'land' set to false.")
                elif region[1] and len(region) == 3: # Rule three
                    raise ValueError("Region " + region[0] + " has a land value" \
                                      " of 'true' but only two truth values.")
            elif 'coast' in region[0].lower() and region[1] is False and region[2]:
                print(region[0] + " is a coast.")
            elif region[1] and len(region) == 4:
                print(region[0] + " is a province.")
            elif region[1] is False and len(region) == 2:
                print(region[0] + " is a sea.")
            else:
                print("Something strange happened with " + region[0] + ".")
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
            if region[1] is False and len(region) == 2:
                return True  
            elif region[1] and region[2]:
                return True
            elif 'coast' in region[0].lower() and region[1] is False and region[2]:
                return True
            else:
                return False
        def is_sea(region):
            """Verifies that a given region is a sea."""
            if 'coast' not in region[0] and region[1] is False and len(region) == 2:
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
                if is_sea_coastal_coast(region) is False:
                    raise ValueError(str(region) + " is in the borders of " \
                                         borders[sea] + "when it is not coded as" \
                                         "a sea, coast, or coastal region."
                                         
# If A borders B and B borders C and C borders A, ABC are all mutually connected.

# If a region is coastal, it necessarily borders at least one sea region.

# All regions bordering a sea are coastal.

# If land is false a second element means it is a supply center coast.

# Sea regions are only supply centers if they're a coast.        
