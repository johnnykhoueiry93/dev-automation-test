# Introduction

For this project, I implemented an AWS EC2 instance consisting of Ubuntu 20 amd64.

Throughout the document, some instructions will be provided regarding how to reach this public server and how to run on a local machine in case needed.

# Tasks Overview
- Task 1 and task 2: Will be covered by the `docker-compose.yml`
- Task 3 and task 4: Will be covered by the python script `deploy.py`
- Task 5: Will be covered by `init_database.groovy` and `init_database.xml`
- Task 6 and task 7: Will be covered by `run_migrations.groovy`, `run_migrations.xml` and `insertIntoMigrations.py`
- Task 8 and Task 9: Will be covered by the python script `deploy.py` 

# AWS Public Instance Setup
Inbound ports 8080 were open to allow binding. This instance is public and reachable:
- Browser: http://3.82.173.95:8080/
  - Credentials will be provided separately
- ssh: through putty
  - user: ubuntu
  - sudo su (no pass)
  - a private key .ppk will be provided separately to allow access

# Requirements Before Setup
For the first time setup, we need to make sure that our environment supports deploying this project.
- `python3`
-  `pip3`
-  python3 MySQL connector `mysql-connector-python-rf`
-  Docker Engine [How to install Docker engine](https://docs.docker.com/engine/install/ubuntu/)
-  Docker Compose [How to install Docker compose](https://docs.docker.com/compose/install/)

# First Time Setup

**Make sure you are running as root**

`whoami` --> root


### AWS Instance Setup
- Connect using putty ssh (login as: `ubuntu`)
- Go to project directory `cd /home/ubuntu/alayaCare`
- Startup the project in detach mode `docker-compose up -d`
- Verify containers are up `docker ps`
- Connect to machine through browser [Jenkins](http://3.82.173.95:8080/)
- user/pass provided privately

### Local Machine Setup
- Create a local directory `mkdir alayaCare`
- Place all the provided files under `alayaCare`
- Update the jenkins container in the `docker-compose.yml` to point to your local machine
   - From `'8080:8080'` to `'127.0. 0.1:8080:8080'`
- Startup the project in detach mode `docker-compose up -d`
- Verify containers are up `docker ps`
- Connect to machine through browser on http://localhost:8080
- To get the password of the jenkins for first time install `docker logs alayacare_jenkins_1`
- Install recommended plugins
- Create a user/pass
- Copy the `database.sql` to `alayacare_jenkins_1`
- Copy the `insertIntoMigrations.py` to `alayacare_jenkins_1`

docker cp database.sql <jenkins_container_id>:/home/
docker cp insertIntoMigrations.py <jenkins_container_id>:/home/

_The copy can be executed by the `deploy.py` script. Jumpt to the section to see how._


# Configure the Jenkins Job
### init_database
- Go to Jenkins
- New Item > name as `init_database`
- Select `Pipeline`
- Configure
   - Definition: Pipeline script
   - Paste the script `run_migrations.groovy`


### run_migrations
- Go to Jenkins
- New Item > name as `run_migrations`
- Select `Pipeline`
- Configure:
   - Check `This project is parameterized`
      - Add a `String Paramter` called `TENANT_NAMES`
      - Add a `String Paramter` called `MIGRATION_NAME`
      - Add a `Choice Paramter` called `RUN_TYPE` with values `sequential` and `parallel`
   - Definition: Pipeline script
   - Paste the script `run_migrations.groovy`


# Job Usage
### init_database
- Simple job, will require only building the database
- Jenkins > Dashboard > init_database >  Build Now
- The job will restore the database to its initial state and data.
- Will override any manually entered or `run_migrations` data input

### run_migrations
- Requires three user inputs
- Jenkins > Dashboard > init_database >  Build with Parameters > Build

**Test 1:**
- tenant1,tenant2,tenant3,tenant4,tenant5,tenant6,tenant7,tenant8,tenant9,tenant10
- mig12
- sequential

**Test 2:**
- ALL
- mig12
- sequential

**Test 3:**
- tenant1,tenant2,tenant3,tenant4,tenant5,tenant6,tenant7,tenant8,tenant9,tenant10
- mig12
- parallel

**Test 4:**
- ALL
- mig12
- parallel

# Deployer Usage
This part will cover the usage of `deploy.py`

Some defensive mechanism where build in to make sure the user entries are correct and follow the code structure.

Addtional help is also provided knowing that this script will handle some of the tasks mentioned in the earlier tasks

python.py's functionalities are defined as follows:
- help: provides manual for usage
- check-migration: displays if tenant has any migration compared to an input (task #8)
- count-migrations: displays the count of migrations per tenant (task #9)
- transfer-to-container: transfers any file from host to a specific container's directory (task #3)
- export-job-config: export job config file from a container to host local directory (task #4)

### Usage
- `python3 deploy.py help `
- `python3 deploy.py check-migration migr2`
- `python3 deploy.py count-migrations`
- `python3 deploy.py transfer-to-container`
- `python3 deploy.py export-job-config`


_Any incorrect/missing argument will exit the deployer while providing the user with a root cause depending on the option(s)_


  
