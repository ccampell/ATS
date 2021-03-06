"""
ATS.py
Calculates and displays the requested statistical information for the Appalachian Trail Data Set.
@Author: Chris Campell
@Version: 7/7/2016
"""
import sys
import os
import json

class ATS(object):

    """
    __init__ -Default constructor for objects of type ATS.
    """
    def __init__(self):
        self.populateShelters()

    """
    populateShelters -Updates self.shelters to contain the list of pre-recorded shelter names and locations. Uses the
        file validated_shelters.csv for recorded shelters.
    Note: Shelter names are stored lower case for substring comparison later on.
    """
    def populateShelters(self):
        self.shelters = {}
        at_shelter_path = "C:/Users/Chris/Documents/GitHub/ATS/Data/Shelter_Data/validated_shelters.csv"
        fp = open(at_shelter_path, 'r')
        line_num = 0
        for line in iter(fp):
            if not line_num == 0:
                split_string = str.split(line, sep=",")
                shelter_name = split_string[0]
                data_set = split_string[1]
                lat = float(split_string[2])
                lon = float(split_string[3])
                type = split_string[4]
                self.shelters[str.lower(str(shelter_name))] = {'num': 0, 'dataset': data_set, 'type': type, 'lat': lat, 'lon': lon}
            line_num += 1
        fp.close()

    """
    isLoggedShelter -Determines if the shelter is already in the list of known shelters.
    :param shelter_name -The name of the shelter to check existence of.
    :return isLoggedShelter -True if shelter is already known, false otherwise.
    """
    def isLoggedShelter(self, shelter_name):
        lookupKey = None
        isLoggedShelter = False
        shelter_name = str.lower(shelter_name)
        num_quotes = shelter_name.count("\"", 0, len(shelter_name))
        shelter_name = shelter_name.replace("\"", "", num_quotes)
        # Preliminary Work, Convert list of shelters to lower case:
        lower_case_shelters = {}
        for shelter, info in self.shelters.items():
            lower_case_shelters[str.lower(shelter)] = self.shelters[shelter]
        # Simple string equality check:
        for key in lower_case_shelters.keys():
            if shelter_name == key:
                lookupKey = shelter_name
                isLoggedShelter = True
                break
            elif shelter_name in key:
                lookupKey = key
                isLoggedShelter = True
                break
            elif key in shelter_name:
                lookupKey = key
                isLoggedShelter = True
                break
            else:
                # TODO: Code more complex substring equality checks.
                # Try search with removal of word "shelter", addition of the word "shelter", etc...
                lookupKey = shelter_name
        return (isLoggedShelter, lookupKey)

    """
    fileLineCount -Counts the number of lines in a given file.
        @param fname -The name of the file from which to count line numbers.
    """
    def fileLineCount(self, fname):
        with open(fname) as file:
            for i, l in enumerate(file):
                pass
            return i + 1

    """
    getShelterStats -Records the number of times each shelter appears in the data set.
    @return void -Upon completion, self.shelters['key']['num'] is updated with the # of times each shelter was visited.
    """
    def getShelterStats(self):
        print("ATS: Gathering Shelter Statistics...")
        num_hikers = 0
        total_num_hikers = self.fileLineCount("at-hikers.txt")
        storage_location = "C:/Users/Chris/Documents/GitHub/ATS/Data/Hiker_Data"
        cwd = os.getcwd()
        with open("at-hikers.txt", 'r') as hikers:
            for line in iter(hikers):
                # print("Gathering Shelter Statistics: " + str(((num_hikers/total_num_hikers)*100)), " percent complete.   \r")
                hiker_fname = storage_location + "/" + str.strip(line, '\n') + ".json"
                os.chdir(storage_location)
                if not os.path.isfile(hiker_fname):
                    print("ATS: Hiker File: %s could not be found. Continuing anyway." % hiker_fname)
                try:
                    with open(hiker_fname, 'r') as hiker:
                        hiker_data = json.load(fp=hiker)
                        hiker_journal = hiker_data['journal']
                        last_dest = None
                        for key in hiker_journal.keys():
                            entry = hiker_journal[key]
                            start_loc = entry['start_loc']
                            dest = entry['dest']
                            if start_loc is not None:
                                start_loc = str.lower(start_loc)
                                shelterLoggedInfo = self.isLoggedShelter(start_loc)
                                if not shelterLoggedInfo[0]:
                                    self.shelters[start_loc] = {'lat': None, 'lon': None, 'num': 1}
                                else:
                                    self.shelters[shelterLoggedInfo[1]]['num'] += 1
                            if dest is not None:
                                dest = str.lower(dest)
                                shelterLoggedInfo = self.isLoggedShelter(dest)
                                if not shelterLoggedInfo[0]:
                                    self.shelters[dest] = {'lat': None, 'lon': None, 'num': 1}
                                else:
                                    self.shelters[shelterLoggedInfo[1]]['num'] += 1
                                last_dest = dest
                    num_hikers += 1
                except:
                    num_hikers += 1
            # print("")
        os.chdir(cwd)

    def sortShelterStats(self):
        pass

    """
    writeShelterStats -Writes
    """
    def writeShelterStats(self):
        outputfile_name = "ATS.csv"
        with open(outputfile_name, 'w') as fp:
            fp.write("shelter,number,lat,lon\n")
            for key, value in self.shelters.items():
                try:
                    lat = value['lat']
                    lon = value['lon']
                except:
                    lat = "None"
                    lon = "None"
                fp.write("\"" + str(key) + "\"," + str(value['num']) + "," + str(value['lat']) +
                         "," + str(value['lon']) + "\n")

    """
    printShelterStats -Prints the obtained statistics regarding AT shelter usage.
    """
    def printShelterStats(self):
        outputString = ""
        for key, value in self.shelters.items():
            outputString += "Shelter: " + str(key) + ", Seen: " + str(value['num']) + " times.\n"
        print(outputString)

"""
main -Default main method.
@param cmd_args -Default command line arguments provided by sys.argv.
"""
def main(cmd_args):
    trail_stats = ATS()
    trail_stats.getShelterStats()
    trail_stats.writeShelterStats()

if __name__ == '__main__':
    main(sys.argv)
