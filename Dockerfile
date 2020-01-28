FROM centos:centos7

RUN yum -y update && \
    yum -y install vim && \
    yum -y install git && \
    yum -y install epel-release && \
    yum -y install python-pip
    
ADD startup.sh /etc/scrpt/startup.sh
ADD packages.sh /etc/scrpt/startup.sh

CMD ["etc/scrpt/startup.sh"]
