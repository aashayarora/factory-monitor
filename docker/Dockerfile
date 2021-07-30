FROM opensciencegrid/software-base:fresh
LABEL maintainer OSG Software <help@opensciencegrid.org>

RUN yum -y install python-pip

ADD requirements.txt /
RUN pip install -r requirements.txt

ADD image-config.d /etc/osg/image-config.d/
ADD monitor /etc/cron.d/monitor
ADD condor-elasticsearch /etc/condor-elasticsearch/
