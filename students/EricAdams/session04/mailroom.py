#!/usr/bin/env python3

"""
Used Chris's solution to session 3 version and added to it to create this,
(session 4) version

Mailroom Exercise -- as of Session 4--  dictionaries yes  Exceptions no

Note: this is not the most robust or flexible code -- but it does the
job with the simplest of Python data structures.

Adding dictionaries
Adding function send_thank_you_to_file.
"""

from textwrap import dedent  # nifty utility!
import sys
import math

# In memory representation of the donor database
# using a tuple for each donor
# -- kind of like a record in a database table
# the donations are in a list -- so you can add to them
# Note the mutable inside an immutable .. that is inside a mutable!


# Making this a global, so it can be accessed from various functions
donor_db = {"William Gates, III": [653772.32, 12.17],
            "Jeff Bezos": [877.33],
            "Paul Allen": [663.23, 43.87, 1.32],
            "Mark Zuckerberg": [1663.23, 4300.87, 10432.0]}


# loop through the donor list and print the 0th element of the list
def print_donors():
    """
    loop through the donor list and print the 0th element of the list
    which is the donors name
    donor name is now the key, since changing over to dict
    """

    print("Donor list:\n")
    for donor in donor_db.keys():
        print(donor)


def find_donor(name):
    """
    Find a donor in the donor db

    :param: the name of the donor

    :returns: The donor data structure -- None if not in the donor_db
    """
    donor = name.lower()
    for key in donor_db.keys():
        # do a case-insenstive compare
        if donor == key.strip().lower():
            return key
        else:
            return None


def main_menu_selection():
    """
    Print out the main application menu and then read the user input.
    """
    # detent is helpful here so you can use a triple quoted string
    action = input(dedent('''
      Choose an action:

      't' - Send a Thank You
      'r' - Create a Report
      'f' - Send Thank You to a file
      'q' - Quit

      > '''))
    return action.strip()


def gen_letter(donor):
    """
    Generate a thank you letter for the donor

    :param: donor tuple

    :returns: string with the entire letter
    """
    return dedent('''
          Dear {}

          Thank you for your very kind donation of ${:.2f}.
          It will be put to very good use.

                         Sincerely,
                            -The Team
          '''.format(donor, donor_db[donor][-1]))


def send_thank_you():
    """
    Execute the logic to record a donation and generate a thank you message.
    """
    # Read a valid donor to send a thank you from, handling special commands to
    # let the user navigate as defined.
    while True:
        name = input("Enter a donor's name "
                     "(or 'list' to see all donors or 'menu' to exit)> "
                     ).strip()
        if name == "list":
            print_donors()
        elif name == "menu":
            return
        else:
            break

    # Now prompt the user for a donation amount to apply. Since this is
    # also an exit point to the main menu, we want to make sure this is
    # done before mutating the donors list object.
    while True:
        amount_str = input(
            "Enter a donation amount (or 'menu' to exit) > ").strip()
        if amount_str == "menu":
            return
        # Make sure amount is a valid amount before leaving the input loop
        amount = float(amount_str)
        # NOTE: this is getting a bit carried away...
        #       maybe better to put in its own function
        if math.isnan(amount) or math.isinf(amount) or round(amount,
                                                             2) == 0.00:
            print("error: donation amount is invalid\n")
            continue  # not really needed, but makes it more clear
        else:
            break

    # If this is a new user, ensure that the database has the necessary
    # data structure.
    donor = find_donor(name)
    if donor is None:
        donor = name
        donor_db[donor] = []

    # Record the donation
    # Note how the donor object can be manipulated while it is in the donors
    # list.
    donor_db[donor].append(amount)

    print(gen_letter(donor))
    send_thank_you_to_file(donor)


def sort_key(item):
    """ key function used to sort the list by first (not zeroth) item"""
    return item[1]


def print_donor_report():
    """
    Generate the report of the donors and amounts donated.
    """
    # First, reduce the raw data into a summary list view
    report_rows = []
    for name in donor_db.keys():
        gifts = donor_db[name]
        total_gifts = sum(gifts)
        num_gifts = len(gifts)
        avg_gift = total_gifts / num_gifts
        report_rows.append((name, total_gifts, num_gifts, avg_gift))

    # sort the report data
    report_rows.sort(key=sort_key)
    # print it out in with a nice format.
    print("{:25s} | {:11s} | {:9s} | {:12s}".format(
          "Donor Name", "Total Given", "Num Gifts", "Average Gift"))
    print("-" * 66)
    for row in report_rows:
        print("{:25s}   {:11.2f}   {:9d}   {:12.2f}".format(*row))


def send_thank_you_to_file(donor):
    """
    Writes the thank you letter to a file with file name = donor.txt
    :param donor
    :return none
    """
    file_name = donor + '.txt'
    f = open(file_name, 'w')
    text = gen_letter(donor)
    f.write(text)
    f.close()


# added an input dictionary.


input_db = {'t': send_thank_you, 'r': print_donor_report, 'q': sys.exit}
if __name__ == "__main__":
    running = True
    while running:
        selection = main_menu_selection()
        input_db[selection]()
