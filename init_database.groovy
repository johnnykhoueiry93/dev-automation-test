def DATABASE_PASSWORD = "mHsJ33lF+1FZ"
def SQL_FILE_PATH = "/home/database.sql"
def HOST="alayacare_db_1"

pipeline {
  agent any
  stages {
    stage('Run SQL File') {
      steps {
      
        sh "mysql -h ${HOST} -p${DATABASE_PASSWORD} < ${SQL_FILE_PATH}"
        
      }
    }
  }
}