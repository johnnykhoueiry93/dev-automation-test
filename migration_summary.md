# Migrations Summary

`python3 deploy.py help`

############################################################

Welcome to Python CLI for AlayaCare Automation Skill Test

############################################################


To check the migrations: python3 deploy.py check-migration input

To count the migrations: python3 deploy.py count-migrations

To push files to a container: python3 deploy.py transfer-to-container

To export Jenkins job configs: python3 deploy.py export-job-config

# State of tenant migrations
`python3 deploy.py count-migrations`

Counting the migrations

tenant1: 8

tenant2: 8

tenant3: 8

tenant4: 8

tenant5: 8

tenant6: 7

tenant7: 6

tenant8: 5

tenant9: 6

tenant10: 6

tenant11: 5

tenant12: 5

tenant13: 5

tenant14: 4

tenant15: 5

tenant16: 5

tenant17: 5

tenant18: 5

tenant19: 5

tenant20: 4


# Tenants with mismatching numbers
`python3 deploy.py check-migration migr5`

Checking the migrations

tenant1: OK

tenant2: OK

tenant3: OK

tenant4: OK

tenant5: OK

tenant6: OK

tenant7: OK

tenant8: OK

tenant9: OK

tenant10: OK

tenant11: OK

tenant12: OK

tenant13: OK

tenant14: missing

tenant15: OK

tenant16: OK

tenant17: OK

tenant18: OK

tenant19: OK

tenant20: OK


We believe that the original `database.sql` might have missed some of the tenants causing this issue. 
However, this can be easily fixed by running the `run_migrations` job and inserting the missing tenants. That should sync up the missing ones.
