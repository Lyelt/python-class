# Nicholas Ghobrial - Final Exam Program
# passmerger

import sys
import sqlite3
import os.path

def getInput() :
    if len(sys.argv) != 2 :
        print("Please enter one command line argument - the name of the database file.")
        sys.exit()
    if not os.path.exists(sys.argv[1]) :
        print(sys.argv[1] + " is not a valid filename.")
        sys.exit()
        
    
def mergeDB() :
    db = sqlite3.connect(sys.argv[1])
        
    curs = db.cursor()
    curs.execute("create table if not exists 'Table3' (Username text, Pass text, Location text, unique (Username))")
    
    # Include system account in first table
    curs.execute("insert or ignore into Table3 select * from Table1 where Username like 'system%'")
    # Include unique to first table
    curs.execute("insert or ignore into Table3 select * from Table1 where Username not in (select Username from Table2)")
    # Include unique to second table, except system account
    curs.execute("insert or ignore into Table3 select * from Table2 where Username not in (select Username from Table1) and Username not in (select Username from Table2 where Username like 'system%')")
    
    # Insert all the things that are in both tables, then update accordingly
    curs.execute("select * from Table1 where Username in (select Username from Table2)")
    rows = curs.fetchall()
    #print(rows)
    for row in rows :
        # Append _1 to name and 1_ to location if it came from Table 1
        curs.execute("insert or ignore into Table3 (Username, Pass, Location) values ('" + str(row[0]).strip("',()") + "_1', '" + str(row[1]).strip("',()") + "', '1_" + str(row[2]).strip("',()") + "')")
    
    curs.execute("select * from Table2 where Username in (select Username from Table1)")
    rows = curs.fetchall()
    #print(rows)
    for row in rows :
        # Append _2 to name and 2S_ to location if it came from Table 2
        curs.execute("insert or ignore into Table3 (Username, Pass, Location) values ('" + str(row[0]).strip("',()") + "_2', '" + str(row[1]).strip("',()") + "', '2_" + str(row[2]).strip("',()") + "')")    
    
    db.commit()
    db.close()
    print("Data merged successfully.")
    
getInput()
mergeDB()