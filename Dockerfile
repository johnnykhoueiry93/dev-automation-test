From jenkins/jenkins:lts
USER root
RUN apt-get -y update && apt-get -y install python3 && apt-get -y install mysql-client && apt -y install python3-pip && pip3 install mysql-connector-python-rf
