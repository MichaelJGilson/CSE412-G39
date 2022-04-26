#!/usr/bin/python3
import psycopg2
from psycopg2 import Error
import pandas as pd
import os

try:
    # Connect to an existing database
    connection = psycopg2.connect(user="michael",
                                  password="",
                                  host="127.0.0.1",
                                  port="8888",
                                  database="coviddata")

    # ----------------------------------------------------------------------------------------------------------------
    # Create a cursor to perform database operations (US LIVE) -------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------
    cursor = connection.cursor()

    cursor.execute(
        """SELECT date, county, state, fips, cases, deaths FROM uscountieslive;""")
    data = cursor.fetchall()

    cols = []
    for elt in cursor.description:
        cols.append(elt[0])

    df = pd.DataFrame(data=data, columns=cols)

    df.to_html("USClive.html", index=False)

    # ----------------------------------------------------------------------------------------------------------------
    # Create a cursor to perform database operations (US TOTAL) ------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------

    cursor.execute(
        """SELECT date, county, state, fips, cases, deaths FROM uscounties LIMIT 20000;""")
    data = cursor.fetchall()

    cols = []
    for elt in cursor.description:
        cols.append(elt[0])

    df = pd.DataFrame(data=data, columns=cols)

    df.to_html("USC.html", index=False)

    html_file = df.to_html()

    # ----------------------------------------------------------------------------------------------------------------
    # Create a cursor to perform database operations (US RECENT) -----------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------

    cursor.execute(
        """SELECT date, county, state, fips, cases, deaths FROM uscountiesrecent LIMIT 20000;""")
    data = cursor.fetchall()

    cols = []
    for elt in cursor.description:
        cols.append(elt[0])

    df = pd.DataFrame(data=data, columns=cols)

    df.to_html("USCrecent.html", index=False)

    html_file = df.to_html()

    # ----------------------------------------------------------------------------------------------------------------
    # Append the 3 databases into one final HTML ---------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------

    filenames = ['header.txt', 'USClive.html', 'header2.txt',
                 'USC.html', 'header3.txt', 'USCrecent.html']
    with open('index.html', 'w') as outfile:

        for names in filenames:

            with open(names) as infile:

                outfile.write(infile.read())

        outfile.write("      </div></body></html>")

    os.remove("USC.html")
    os.remove("USClive.html")
    os.remove("USCrecent.html")

except (Exception, Error) as error:
    print("Error: ", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
