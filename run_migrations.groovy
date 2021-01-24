pipeline {
    agent any
    stages {
        stage('Run SQL File') {
            steps {
                print "DEBUG: parameter TENANT_NAMES = ${TENANT_NAMES}"
                print "DEBUG: parameter MIGRATION_NAME = ${MIGRATION_NAME}"

                script {
                    def DATABASE_PASSWORD = 'mHsJ33lF+1FZ'
                    def SQL_FILE_PATH = '/home/database.sql'
                    def HOST = 'alayacare_db_1'
                    
                    def filelist=null
                    if("$RUN_TYPE" == "sequential") {
                        filelist = getChangedFilesList() // Get the array of tenants
                        for ( def elem in filelist ) { 
                            sh "python3 /home/insertIntoMigrations.py $elem $MIGRATION_NAME $RUN_TYPE"
                        }  
                    } else {
                            sh "python3 /home/insertIntoMigrations.py '$TENANT_NAMES' $MIGRATION_NAME $RUN_TYPE"
                    }
                }
            }
        }
    }
}

@NonCPS
def getChangedFilesList() {
    String csvTenantNames = "${TENANT_NAMES}"
    String[] arrayTenantNames
    arrayTenantNames = csvTenantNames.split(',')

    return arrayTenantNames
}

def insertTenantIntoDatabase(String myElem)
{
    print "DEBUG: We are in insertTenantIntoDatabase function!!"

    def SQL = "SELECT name FROM tenants;"
    def CMD = "mysql rmtest -pmHsJ33lF+1FZ <<-EOF\n${SQL}\nEOF"
    sh "${CMD}"
}