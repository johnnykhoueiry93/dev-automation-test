from multiprocessing import Pool
from multiprocessing.pool import ThreadPool  # uses threads, not processes
import multiprocessing
import mysql.connector
import itertools
import sys
import logging
from threading import Thread


def datavaseConnection():
    mydb = mysql.connector.connect(
        host="alayacare_db_1",
        user="root",
        password="mHsJ33lF+1FZ",
        database="rmtest"
    )

    return mydb


def convertTuple(tup):
    # required for ALL + parallel execution
    str = ''.join(tup)
    return str


def loadSingleTenantSequentially(tenantName, migrationName):
    mydb = datavaseConnection()
    sql = "INSERT INTO migrations(tenant_id, name) VALUES (%s, %s)"
    mycursor = mydb.cursor()
    logging.debug("DEBUG: Searching for " + tenantName + " ID")
    mycursor.execute("SELECT id FROM tenants where name ='" + tenantName+"'")
    tenantId = mycursor.fetchall()

    if len(tenantId) < 1:
        logging.debug("DEBUG: Sorry this tenant: " + tenantName +
                      " in not available in our database records!")
    else:
        for tenant in tenantId:
            val = (tenant[0], migrationName)
            mycursor.execute(sql, val)
            mydb.commit()
            logging.debug("DEBUG: Inserting " + tenantName + "'s ID: " +
                          str(tenant[0]) + " into the database")
            logging.debug(
                "DEBUG: SUCCESS - 1 record inserted - ID:" + str(mycursor.lastrowid))


def loadAllTenantsToMigrationTableSequentially():
    print("Loading all tenants from the database")
    mydb = datavaseConnection()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT name FROM tenants")
    myresult = mycursor.fetchall()
    logging.debug("DEBUG: Found available " +
                  str(len(myresult)) + " tenants to be added!")

    for tenant in myresult:
        loadSingleTenantSequentially(tenant[0], sys.argv[2])


def loadTenantsParalle(array):
    try:
        logging.debug("Function: loadTenantsParalle")
        logging.debug("Received array is:" + str(array))
        mydb = datavaseConnection()
        sqlInsert = "insert into migrations (tenant_id, name) values ({0}),'{1}')".format(
            array, sys.argv[2])
        mycursor = mydb.cursor()
        mycursor.execute(sqlInsert)
        mydb.commit()
        mycursor.close()
        mydb.close()

        logging.debug("DEBUG: Exiting Thread responsible for: {0}")

    except Exception as e:
        logging.debug("ERROR: Exception: %s" % e)


def sequential():
    if sys.argv[1] == "ALL":
        loadAllTenantsToMigrationTableSequentially()
    else:
        loadSingleTenantSequentially(sys.argv[1], sys.argv[2])


def parallel(arr):
    # https://pythontic.com/database/mysql/connection%20pooling
    migrationBathSize = 5
    logging.debug("Number of available processors: " +
                  str(multiprocessing.cpu_count()))
    if multiprocessing.cpu_count() < migrationBathSize:
        logging.debug("WARNING: Your system has only " +
                      str(multiprocessing.cpu_count()) + " processors!")
    logging.debug(arr)

    iterableList = list()

    if(arr == "ALL"):
        logging.debug(arr)
        mydb = datavaseConnection()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT name FROM tenants")
        myresult = mycursor.fetchall()
        for result in myresult:
            iterableList.append(result)
    else:
        iterableList = list(arr.split(","))
        logging.debug(iterableList)

    threadCollection = []
    array = []

    # Will return array of arrays of 5's
    for i in range(0, len(iterableList), migrationBathSize):
        array.append(iterableList[i:i+migrationBathSize])
        logging.debug(array)

        for j in array:  # Will return first array of 5
            logging.debug("Sending the thread with the element: " + str(j))

            for k in j:  # Will loop over each of the 5 items
                logging.debug("Running Thread " + str(k))
                t = Thread(target=loadSingleTenantSequentially,
                           args=(convertTuple(k), sys.argv[2]))
                threadCollection.append(t)

                t.start()

    for thread in threadCollection:
        thread.join()


def main():
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
    logging.debug("User selected the execution mode: " + sys.argv[3])

    if sys.argv[3] == "sequential":
        sequential()
    elif sys.argv[3] == "parallel":
        parallel(sys.argv[1])


if __name__ == "__main__":
    main()
