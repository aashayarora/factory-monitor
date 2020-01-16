FROM centos:centos7

RUN yum -y install vim && \
    yum -y install git

ADD startup.sh /home/

#CMD ["/home/startup.sh"]
