FROM centos:centos7

RUN yum -y update && \
    yum -y install vim && \
    yum -y install git && \
    yum -y install epel-release && \
    yum -y install python-pip
 
ADD image-config.d /etc/image-config.d/

CMD ["bin/bash", "-c", "for x in /etc/image-config.d/*.sh; do source "$x"; done"]

