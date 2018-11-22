import sqlite3
import argparse
import statistics
import math


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Prison Simulator Metric Generator')
    group = parser.add_argument_group("Required Arguments")
    group.add_argument("-s", "--simulationid", help="ID Of the Simulation executed", required=True)

    args = parser.parse_args()
    simulation_id = args.simulationid

    db_path = "./simulations.db"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query0 = "SELECT MAX(ps.day_count)" \
             " FROM prisoner_stat ps" \
             " WHERE ps.simulation_id = {simulation_id}"
    query0 = query0.format(simulation_id=simulation_id)
    cursor.execute(query0)
    total_days = cursor.fetchone()[0]
    print("Total Number Of Days Before Announcement Was Made: " + str(total_days))


    query1 = "SELECT AVG(a.first_visit_day) AS average_wait_per_prisoner" \
             " FROM (" \
             "         SELECT ps.prisoner_id, MIN(ps.day_count) AS first_visit_day" \
             "         FROM prisoner_stat ps" \
             "         WHERE ps.has_visited_before = 1 AND ps.simulation_id = {simulation_id}" \
             "         GROUP BY ps.prisoner_id" \
             "      ) a"
    query1 = query1.format(simulation_id=simulation_id)


    cursor.execute(query1)
    average = cursor.fetchone()[0]
    print("Average Number of Days Before First Visit By Each Prisoner Is: " + str(average) + " Days")

    '''
    query2 = "SELECT ps.prisoner_id, MIN(ps.day_count) AS first_visit_day" \
             " FROM prisoner_stat ps" \
             " WHERE ps.has_visited_before = 1 AND ps.simulation_id = {simulation_id}" \
             " GROUP BY ps.prisoner_id" \
             " ORDER BY first_visit_day"
    query2 = query2.format(simulation_id=simulation_id)
    cursor.execute(query2)

    prisoners = cursor.fetchall()
    '''

    query3 = "SELECT ps.prisoner_id, ps.prisoner_visit_count, MIN(ps.day_count) AS visit_day" \
             " FROM prisoner_stat ps" \
             " WHERE ps.is_counter = 1 AND ps.simulation_id = {simulation_id}" \
             " GROUP BY ps.prisoner_visit_count" \
             " ORDER BY visit_day"
    query3 = query3.format(simulation_id=simulation_id)
    cursor.execute(query3)
    visit_days = []
    for row in cursor.fetchall():
        visit_days.append(int(row[2]))

    deltas = []
    smallest_delta = None
    largest_delta = None
    for i in range(0, len(visit_days)-1):
        delta = abs(visit_days[i+1] - visit_days[i])
        deltas.append(delta)

        if smallest_delta is None:
            smallest_delta = delta
        elif delta < smallest_delta:
            smallest_delta = delta

        if largest_delta is None:
            largest_delta = delta
        elif delta > largest_delta:
            largest_delta = delta

    variance = 0
    mean = statistics.mean(deltas)
    for delta in deltas:
        variance += ((delta - mean)**2)
    standard_deviation = math.sqrt(variance)

    values_within_variance = 0
    for delta in deltas:
        if delta < (mean + standard_deviation) and delta > (mean - standard_deviation):
            values_within_variance += 1
    percent_within_variance = (values_within_variance / len(deltas) * 100)

    print("The Average Time Between Visits By The Counter Was: " + str(statistics.mean(deltas)) + " Days")
    print(" - Variance: " + str(variance))
    print(" - Standard Deviation: " + str(standard_deviation))
    print(" - Percentage Within 1 Standard Deviation Of The Average (What Percent Of Numbers Are Close To The Average): " + str(percent_within_variance))


    query4 = "SELECT MAX(ps.total_lightswitch_flips), MAX(ps.total_lightswitch_flips_off), MAX(ps.total_lightswitch_flips_on)" \
             " FROM prisoner_stat ps" \
             " WHERE ps.simulation_id = {simulation_id}"
    query4 = query4.format(simulation_id=simulation_id)
    cursor.execute(query4)

    result = cursor.fetchone()
    total_lightswitch_flips = result[0]
    total_lightswitch_flips_off = result[1]
    total_lightswitch_flips_on = result[2]
    print("The Total Number Of LightSwitch Flips Was: " + str(total_lightswitch_flips) + " Flips")
    print(" - Total Flips Off: " + str(total_lightswitch_flips_off))
    print(" - Total Flips On: " + str(total_lightswitch_flips_on))

    query5 = "SELECT AVG(a.total_room_entries), MAX(a.total_room_entries), MIN(a.total_room_entries) " \
             "FROM ( " \
             "          SELECT ps.prisoner_id, MAX(ps.enter_room_count) AS total_room_entries" \
             "          FROM prisoner_stat ps" \
             "          WHERE ps.simulation_id = {simulation_id}" \
             "          GROUP BY ps.prisoner_id" \
             "      ) a"

    query5 = query5.format(simulation_id=simulation_id)
    cursor.execute(query5)
    result2 = cursor.fetchone()

    average_room_entries = result2[0]
    max_room_entries = result2[1]
    min_room_entries = result2[2]

    print("A Prisoner Was Chosen To Go Into The Room An Average Of: " + str(average_room_entries) + " Times")
    print(" - Max Total Room Entries: " + str(max_room_entries))
    print(" - Min Total Room Entries: " + str(min_room_entries))


    query6 = "SELECT DISTINCT ps.prisoner_id FROM prisoner_stat ps WHERE ps.simulation_id = {simulation_id}"
    query6 = query6.format(simulation_id=simulation_id)
    cursor.execute(query6)

    prisoner_averages = []
    for prisoner_row in cursor.fetchall():
        prisoner_id = prisoner_row[0]

        query7 = "SELECT ps.prisoner_id, ps.enter_room_count, MIN(ps.day_count) AS day_entered" \
                 " FROM prisoner_stat ps " \
                 " WHERE ps.prisoner_id = {prisoner_id} AND ps.simulation_id = {simulation_id}" \
                 " GROUP BY ps.enter_room_count" \
                 " ORDER BY day_entered"
        query7 = query7.format(prisoner_id=prisoner_id, simulation_id=simulation_id)
        cursor.execute(query7)

        prisoner_entered_room_rows = cursor.fetchall()
        deltas = []
        for i in range(0, len(prisoner_entered_room_rows)-1):
            next_row = prisoner_entered_room_rows[i+1][2]
            current_row = prisoner_entered_room_rows[i][2]

            delta = abs(next_row - current_row)
            deltas.append(delta)

        average_visits_for_prisoner = statistics.mean(deltas)
        prisoner_averages.append(average_visits_for_prisoner)

    average_days_between_visit = statistics.mean(prisoner_averages)

    print("The Average Days Between Entering The Room Per Prisoner Is: " + str(average_days_between_visit))







