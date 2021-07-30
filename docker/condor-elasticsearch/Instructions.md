Installing Elasticsearch and RabbitMQ
=====================================
Document made on 29.06.2018

[Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/rpm.html)
---------------
Elasticsearch is a search engine based on Lucene. It provides a distributed,
multitenant-capable full-text search engine with an HTTP web interface and
schema-free JSON documents.
(From Wikipedia's entry on [Elasticsearch](https://en.wikipedia.org/wiki/Elasticsearch))

Make sure a java VM is installed. Elasticsearch needs at least java 8.

Add the Elasticsearch RPM repository. Create a file named elasticsearch.repo
in  the /etc/yum.repos.d/ directory. The file will contain the following:
```
# In /etc/yum.repos.d/elasticsearch.repo
[elasticsearch-6.x]
name=Elasticsearch repository for 6.x packages
baseurl=https://artifacts.elastic.co/packages/6.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
```

Install the Elasticsearch package:
```
yum install elasticsearch
```

Verify if you have init or systemd:
```
ps -p 1
```

If you want elasticsearch to start automatically on system boot execute the
following, if on systemd:
```
systemctl daemon-reload
systemctl enable elasticsearch.service
```

If you want elasticsearch to start automatically on system boot execute the
following, if on init:
```
chkconfig --add elasticsearch
```

Start or stopt the elastic search service, if on systemd:
```
systemctl start elasticsearch.service
systemctl stop elasticsearch.service
```

Start or stop the elastic search service, if on init:
```
service elasticsearch start
service elasticsearch stop
```

Check that elastic search is running by doing an HTTP request:
```
curl -X GET "localhost:9200/"
```

[RabbitMQ](https://www.rabbitmq.com/install-rpm.html)
----------
RabbitMQ is an open source message broker software (sometimes called
message-oriented middleware) that originally implemented the Advanced Message
Queuing Protocol (AMQP) and has since been extended with a plug-in architecture
to support Streaming Text Oriented Messaging Protocol (STOMP), Message Queuing
Telemetry Transport (MQTT), and other protocols.
(From Wikipedia's entry on [RabbitMQ](https://en.wikipedia.org/wiki/RabbitMQ))

Make sure you have a supported version of Erlang. You can check which Erlang
version you need [here](https://www.rabbitmq.com/which-erlang.html). This guide
was made to install RabbitMQ 3.7.7 with Erlang 21.0.x

You can install a stripped down version of Erlang by adding the Erlang repository
by RabbitMQ:
```
# In /etc/yum.repos.d/rabbitmq-erlang.repo
[rabbitmq-erlang]
name=rabbitmq-erlang
# On CentOS 7
baseurl=https://dl.bintray.com/rabbitmq/rpm/erlang/21/el/7
# On CentOS 6
#baseurl=https://dl.bintray.com/rabbitmq/rpm/erlang/21/el/6
gpgcheck=1
gpgkey=https://dl.bintray.com/rabbitmq/Keys/rabbitmq-release-signing-key.asc
repo_gpgcheck=0
enabled=1
```
Install Erlang with yum:
```
yum install erlang
```
Please note that you need libcrypto. If the installation failed because of that,
you can try running:

Download de RabbitMQ server:
```
curl -O -L https://dl.bintray.com/rabbitmq/all/rabbitmq-server/3.7.7/rabbitmq-server-3.7.7-1.el7.noarch.rpm
```

Add the public signing key and install RabbitMQ using yum:
```
rpm --import https://dl.bintray.com/rabbitmq/Keys/rabbitmq-release-signing-key.asc
yum install rabbitmq-server-3.7.7-1.el7.noarch.rpm
```

To start the daemon automatically when the system boots run:
```
chkconfig rabbitmq-server on
```

Start and stop the server as an administrator as follows:
```
/sbin/service rabbitmq-server start
/sbin/service rabbitmq-server stop
```

Verify that rabbitmq is installed:
```
rabbitmqctl status
```

You can't connect remotely with the default user with the default settings.
Create a new user called "jmalanirabbit" with password "ucsdrabbit", and give
permissions to access and modify the default vhost:
```
rabbitmqctl add_user jmalanirabbit ucsdrabbit
rabbitmqctl list_users
rabbitmqctl set_permissions jmalanirabbit ".*" ".*" ".*"
```

The max number of open files is too low for a messaging broker (default 1024,
check with uname -n). RabbitMQ's
installation guide recommends at least 65536 for production environments and
4096 for development workloads. Check the (H)ard and (S)oft limits:
```
ulimit -Hn
ulimit -Sn
```

Look for
the configuration file
/etc/systemd/system/rabbitmq-server.service.d/limits.conf and modify it as
needed (you may need to create the directory and file):
```
[Service]
LimitNOFILE=17408
```

Verify the limit via rabbitmqctl (file descriptors):
```
rabbitmqctl status
```
(If not, the hard limits for the OS may need to be increased. Edit
/etc/security/limits.conf)

Python Elasticsearch and RabbitMQ libraries
--------------------------------------------

To install the Elasticsearch libraries systemwide for python using pip run:
```
pip install --user elasticsearch
pip install --user elasticsearch-dsl
```

To install the RabbitMQ python client (called Pika) run:
```
pip install --user pika
```

Logstash
--------
