FROM centos:centos7

RUN yum -y install vim && \
    yum -y install git && \
    
ADD startup.sh /etc/scrpt/startup.sh

CMD ["/etc/scrpt/startup.sh"]
