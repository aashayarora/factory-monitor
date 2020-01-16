FROM centos:centos7

RUN yum -y install vim && \
    yum -y install git

CMD ["git clone https://github.com/aaarora/condor-elasticsearch.git /home"]
