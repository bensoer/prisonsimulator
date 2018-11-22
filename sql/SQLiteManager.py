import sqlite3



class SQLiteManager:

    db_path = "./simulations.db"

    def __init__(self):

        self._conn = sqlite3.connect(self.db_path)
        self._cursor = self._conn.cursor()

        self._cursor.execute('''CREATE TABLE IF NOT EXISTS prisoner_stat
                            (id INTEGER PRIMARY KEY, simulation_id INTEGER, prisoner_id INTEGER, is_counter INTEGER,
                            prisoner_visit_count INTEGER, has_visited_before INTEGER, day_count INTEGER, 
                            max_prisoners INTEGER, declare_all_prisoners_visited INTEGER, 
                            total_lightswitch_flips INTEGER, total_lightswitch_flips_on INTEGER,
                            total_lightswitch_flips_off INTEGER, enter_room_count INTEGER)''')

        self._conn.commit()

    def addRecordsForPrisoners(self, prisoners, light_switch, simulation_id):

        prisoner_tuples = list()

        for prisoner in prisoners:
            prisoner_tuple = (simulation_id, prisoner.prisoner_number, int(prisoner.is_counter),
                              prisoner.prisoner_visit_count, int(prisoner.has_visited_before),
                              prisoner.day_count, prisoner.max_prisoners, int(prisoner.declare_all_prisoners_visited),
                              light_switch.total_lightswitch_flips, light_switch.total_lightswitch_flips_on,
                              light_switch.total_lightswitch_flips_off, prisoner.enter_room_count)
            prisoner_tuples.append(prisoner_tuple)

        query = "INSERT INTO prisoner_stat (simulation_id, prisoner_id, is_counter, prisoner_visit_count, " \
                "has_visited_before, day_count, max_prisoners, declare_all_prisoners_visited," \
                "total_lightswitch_flips, total_lightswitch_flips_on, total_lightswitch_flips_off," \
                "enter_room_count) " \
                "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        self._cursor.executemany(query, prisoner_tuples)
        self._conn.commit()

    def closeEverything(self):
        try:
            self._cursor.close()
            self._conn.close()
        except:
            pass
