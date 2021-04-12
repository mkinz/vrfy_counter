##########################
##### Verify Counter #####
#########################
# This script will count instances of pptype in a fracture verify log

import re, argparse, sys

def get_regex():
    
    """function that builds a list of iterable regex objects """

    # empty list to store regex objects
    regex_list = []

    # list of pptypes
    cats_list = ["CDM","CDJ","CDN","CTM","CTJ","CTN","CLM","CLJ","CLN"]
    mgc_list = ["MDM","MDJ","MDN","MLM","MLJ","MLN","MCM","MCJ","MCN"]
    both_list = cats_list + mgc_list   #list of all pptypes for both vendors

    # logic to drive mgc or cats for generating list of regex objects
    if args.vendor == 'mgc' or args.vendor == 'MGC':
        pptypes = mgc_list
    elif args.vendor == 'cats' or args.vendor == 'CATS':
        pptypes = cats_list
    elif args.vendor == 'both':
        pptypes = both_list
    else:
        print 'You need to specify a vendor when executing the program, like this: -v mgc or -v cats'
        print 'Please try again...'
        sys.exit(1)
    
    # loop over the list of pptypes, compile regex object for each item, append to regex_list
    for item in pptypes:
        regex = re.compile(".*({}).*".format(item))
        regex_list.append(regex)
    
    return regex_list


def count_by_pptype():
    """ open the fracture verify file, iterate over regex list, iterate over line, 
    and count items that match the regex iterable"""
    try: 
        with open(args.filename, "r") as f:
            count_of_items = {}
            regex = get_regex()    # call the get_regex() function defined above
            mydata = f.read()
            for item in regex:     # iterate over all regex matches
                for line in re.findall(item, mydata):
                    if line not in count_of_items.keys():
                        count_of_items[line] = 0
                    count_of_items[line] += 1
        
            print "count of successful verifications: ", sum(count_of_items.values())
            return count_of_items
    except IOError:
        print "file not found!"
        sys.exit(1)


def main():
    """ main function, calls the other functions"""
        
    # use argparse to get input filename and flag mgc or cats
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="input filename of verify file to count instances of pptype")
    parser.add_argument("-v", "--vendor", choices=['mgc','MGC','cats','CATS', 'both'], type=str, help="fracture vendor")
    args = parser.parse_args()
        
    get_regex()
    print count_by_pptype()


if __name__ == "__main__":
    main()
    
