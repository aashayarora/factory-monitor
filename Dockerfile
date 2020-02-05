FROM opensciencegrid/software-base:fresh
LABEL maintainer OSG Software <help@opensciencegrid.org>

RUN yum -y update && \
    yum -y install vim && \
    yum -y install git && \
    yum -y install epel-release && \
    yum -y install python-pip

ADD image-config.d /etc/osg/image-config.d/
ADD monitor /etc/cron.d/monitor

