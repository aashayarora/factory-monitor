FROM centos:centos7

RUN yum -y install vim && \
    yum -y install git
    
ADD startup.sh /etc/scrpt/startup.sh

CMD git clone https://github.com/aaarora/condor-elasticsearch.git /etc/condor-elasticsearch/
