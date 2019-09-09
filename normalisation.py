import csv
import sys
import pandas as pd
import difflib
import numpy as np


# ignore Levenshtein distance for now. It doesn't affect the computation in anyway . Although, it can be used to improve the program

def levenshtein_distance(first_string, second_string):
    first_string = first_string.strip().lower()
    first_size = len(first_string) + 1

    second_string = second_string.strip().lower()
    second_size = len(second_string) + 1

    # initializing the distance_array as 0
    distance_array = np.zeros((first_size, second_size))

    for i in range(1, first_size):  # valid because first_size = m+1
        distance_array[i][0] = i

    for j in range(1, second_size):  # valid because second_size = n+1
        distance_array[0][j] = j

    # since the subsitution cost is a non zero quantity

    for i in range(1, first_size):
        for j in range(1, second_size):
            if first_string[i - 1] == second_string[j - 1]:
                distance_array[i][j] = min(distance_array[i - 1][j] + 1, distance_array[i - 1][j - 1],
                                           distance_array[i][j - 1] + 1)
            else:
                distance_array[i][j] = min(distance_array[i - 1][j] + 1, distance_array[i - 1][j - 1] + 1,
                                           distance_array[i][j - 1] + 1)

    return distance_array[first_size - 1][second_size - 1]


# The header that have to be set up if the form change
mapping_headers = {
    "year": "Year of Study",
    "name": "Full Name",
    "room_number": "Room Number",
    "gender": "Gender",
    "is_captain": "Are you Captain of a Sport",
    "representing_sports_ivp": "Have you represented NUS (SUNIG/IVP) in the following sports:",
    "sports_currently_in": "Sports you are currently in (after latest cut)",
    "email": "Email Address"
}

sports = {"aquathlon", "badminton", "basketball", "biathlon", "cross country", "floorball", "frisbee", "handball", "lifesaving", "netball", "road relay", "sepak takraw", "soccer", "softball", "squash", "swimming", "table tennis", "tennis", "touch rugby", "track", "triathlon", "volleyball", "water polo"}


def yes_no(string):
    answer = "yes"
    if (difflib.SequenceMatcher(None, answer, string).ratio() > 0.7):
        return 1
    else:
        return 0


final_score = []
is_captain_score_list = []
all_sports_enrolled_in_score_list = []
all_sports_represented_IVP_SUNIG_list = []


def calculate_points_subroutine(iter, the_column, the_set):
    score = 0
    the_cell_partition = str(the_column[iter]).split(";")

    # keep NONE as a option for
    if "none" in the_cell_partition:
        return score

    for sport in the_cell_partition:
        sport = sport.strip().lower()
        for s in the_set:
            if levenshtein_distance(sport, s) <= 3:
                score += 1
                break

    return score


# calculates the final points .. takes into consideration .. the possible
# since a player is a captain of atmost 1 team .. consider yes / no
def calculate_points():
    data_frame = pd.read_csv("SMC_input.csv")
    is_captain_column = data_frame[str(mapping_headers["is_captain"])]
    is_captain_column = is_captain_column.str.lower()
    is_captain_column = is_captain_column.str.strip()

    # stripping all the white spaces and the converting into lower case in the sports column
    sports_column = data_frame[str(mapping_headers["sports_currently_in"])]
    sports_column = sports_column.str.lower()
    sports_column = sports_column.str.strip()

    # stripping all the white spaces and the converting into lower case in the sports_represented  column
    representing_sports_column = data_frame[str(mapping_headers["representing_sports_ivp"])]
    representing_sports_column = representing_sports_column.str.lower()
    representing_sports_column = representing_sports_column.str.strip()

    for iteration in range(len(is_captain_column)):
        score = 0
        score += yes_no(is_captain_column[iteration])
        is_captain_score_list.insert(iteration, score)  # enter 0 or 1 in the is_captain_score Column

        # counting points for all the sports currently involved in
        all_sports_currently_involved_in_score = calculate_points_subroutine(iteration, sports_column, sports)
        # adding the score for number of sports enrolled in the
        all_sports_enrolled_in_score_list.insert(iteration, all_sports_currently_involved_in_score)
        score += all_sports_currently_involved_in_score

        # calc for score on the basis of sports represented in IVP and SUNIG
        all_sports_represented_score = calculate_points_subroutine(iteration, representing_sports_column, sports)
        # adding the score of representing the sport at IVP/SUNIG in the list
        all_sports_represented_IVP_SUNIG_list.insert(iteration, all_sports_represented_score)
        score += all_sports_represented_score

        final_score.insert(iteration, score)

    data_frame["total_points"] = final_score
    data_frame["captain_points"] = is_captain_score_list
    data_frame["sports_enrolled_in_points"] = all_sports_enrolled_in_score_list
    data_frame["sports_represented_points"] = all_sports_represented_IVP_SUNIG_list
    return data_frame

output_df = calculate_points()

# uncomment to test
# print(" FINAL POINTS")
# print(final_score)
# print()
# print("CAPTAIN POINTS")
# print(is_captain_score_list)
# print()
# print(" SPORTS ENROLLED IN POINTS : ")
# print(all_sports_enrolled_in_score_list)
# print()
# print(" ALL SPORTS REPRESENTED : ")
# print(all_sports_represented_IVP_SUNIG_list)
# print()

file_name = 'allocation/normalisation_output.csv'

output_df.to_csv(file_name, sep=',' , encoding='utf-8')
print('Points computed. {} created in allocation folder!'.format(file_name))
