FROM centos:centos7

RUN yum -y update && \
    yum -y install vim && \
    yum -y install git && \
    yum -y install epel-release && \
    yum -y install python-pip

ADD imgconf.sh /etc/scrpt/imgconf.sh    
ADD image-config.d /etc/image-config.d/

CMD etc/scrpt/imgconf.sh
