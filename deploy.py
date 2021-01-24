import sys
import mysql.connector
import os
import subprocess


def datavaseConnection():
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="mHsJ33lF+1FZ",
        database="rmtest"
    )

    return mydb


def runCommad(string):
    command = os.popen(string)
    print(command.read())
    return print(command.read())


def tansferFileToContainer():
    runCommad("docker ps")

    filename = input(
        "Please input the filename you wish to transfer: ")
    containerId = input(
        "Please select the desired container ID from the list above: ")
    containerDirectory = input(
        "Please input the container ID full path directory: ")

    runCommad("docker cp " + filename + " " +
              containerId + ":" + containerDirectory)

    print("The file "+filename+" was copied to the container " +
          containerId + " under " + containerDirectory)


def exportJobConfig():
    runCommad("docker ps")
    containerId = input(
        "Please select the desired container ID from the list above: ")
    jobName = input(
        "Please select the desired job name to export: ")

    runCommad("docker cp " + containerId +
              ":/var/jenkins_home/jobs/" + jobName + "/config.xml .")

    # Rename the file in case 1 job overrides the other
    os.rename("./config.xml", "./"+jobName+"_config.xml")


def pushSQLFileToJenkinsContainer(file, containerId, directory):
    print("Pushing file: " + file + " to the container: " +
          containerId + " under directory: " + directory)


def displayHelp():
    print("To check the migrations: python3 deploy.py check-migration input")
    print("To count the migrations: python3 deploy.py count-migrations")
    print("To push files to a container: python3 deploy.py transfer-to-container")
    print("To export Jenkins job configs: python3 deploy.py export-job-config")


def generateSummaryReport():
    print("Generating report")


def checkMigrations(migration):
    print("Checking the migrations\n")
    mydb = datavaseConnection()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT tenants.name, IF(m.tenant_id IS NULL ,'missing','OK') FROM tenants LEFT JOIN (select * from migrations where migrations.name='" +
                     migration + "') m  ON tenants.id = m.tenant_id ")

    myresult = mycursor.fetchall()
    for tenant in myresult:
        print(tenant[0] + ": " + tenant[1])


def countMigrations():
    print("Counting the migrations\n")
    mydb = datavaseConnection()
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT tenants.name, count(migrations.name) FROM tenants LEFT JOIN migrations  ON tenants.id = migrations.tenant_id GROUP BY tenants.id ORDER BY tenants.id")
    myresult = mycursor.fetchall()
    for tenant in myresult:
        print(tenant[0] + ": " + str(tenant[1]))


def main():
    os.system("clear")
    print("############################################################\n")
    print("Welcome to Python CLI for AlayaCare Automation Skill Test\n")
    print("############################################################\n\n")

    if len(sys.argv) < 2:
        print("You are required to enter a least 1 argument to start!")
        displayHelp
        sys.exit()

    else:

        if sys.argv[1] == "help":
            displayHelp()

        elif sys.argv[1] == "check-migration":
            if len(sys.argv) < 3:
                print("ERROR: This method requires 2 arguments!\n")
            else:
                checkMigrations(sys.argv[2])

        elif sys.argv[1] == "count-migrations":
            countMigrations()

        elif sys.argv[1] == "transfer-to-container":
            tansferFileToContainer()

        elif sys.argv[1] == "export-job-config":
            exportJobConfig()

        else:
            print("I am sorry but this option is not available!\n")
            displayHelp()


if __name__ == "__main__":
    main()
