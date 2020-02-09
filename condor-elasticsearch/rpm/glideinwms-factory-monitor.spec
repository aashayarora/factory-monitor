%define systemddir %{_prefix}/lib/systemd/system

Name:           glideinwms-factory-monitor
Version:        1.5.2
Release:        1%{?dist}
Summary:        Visualizes Condor Factory meta data in Grafana
License:        Apache 2.0

Source0:	%{name}-%{version}.tar.gz
BuildArch:  noarch

Requires: python
Requires: glideinwms-factory

%description
This monitor aggregates data accumulated by the factory and sends it to a database
to be visualized by Grafana. InfluxDB is one of the supported databases.

%pre
getent group factmon >/dev/null || groupadd -r GROUPNAME
getent passwd factmon >/dev/null || \
    useradd -r -g factmon -d HOMEDIR -s /sbin/nologin \
    -c "this user is created to allow for selective use of the service" factmon
exit 0

%prep
%setup -q

%build

%install
mkdir -p $RPM_BUILD_ROOT%{python2_sitelib}/%{name}/{aggregator,config,http,messenger/outbox,crontab}
%if %{?rhel}%{!?rhel:0} == 7
install -d $RPM_BUILD_ROOT/%{systemddir}
install -m 0644 init.d/%{name} $RPM_BUILD_ROOT/%{systemddir}/
%else
install -d $RPM_BUILD_ROOT%{_initrddir}
install -m 0755 init.d/%{name} $RPM_BUILD_ROOT%{_initrddir}/
%endif
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/
mkdir -p $RPM_BUILD_ROOT%{_bindir}/
install -m 777 logrotate/%{name} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/
install -m 644 crontab/%{name} $RPM_BUILD_ROOT%{python2_sitelib}/%{name}/crontab/
install -m 777 monitor.py $RPM_BUILD_ROOT%{_bindir}/
install -m 777 aggregator/*.py $RPM_BUILD_ROOT%{python2_sitelib}/%{name}/aggregator/
install -m 777 config/*.py $RPM_BUILD_ROOT%{python2_sitelib}/%{name}/config/
install -m 777 config/config.json $RPM_BUILD_ROOT%{python2_sitelib}/%{name}/config/
install -m 777 http/*.py $RPM_BUILD_ROOT%{python2_sitelib}/%{name}/http/
install -m 777 messenger/*.py $RPM_BUILD_ROOT%{python2_sitelib}/%{name}/messenger/

%files
%defattr(-,root,root,-)
%if %{?rhel}%{!?rhel:0} == 7
%{systemddir}/%{name}
%else
%{_initrddir}/%{name}
%endif
%{_sysconfdir}/logrotate.d/%{name}
%{python2_sitelib}/%{name}/crontab/%{name}
%{_bindir}/monitor.py*
%{python2_sitelib}/%{name}/aggregator/*.py*
%{python2_sitelib}/%{name}/config/*.py*
%config(noreplace) %{python2_sitelib}/%{name}/config/config.json
%{python2_sitelib}/%{name}/http/*.py*
%{python2_sitelib}/%{name}/messenger/*.py*

%dir %{python2_sitelib}/%{name}/aggregator/
%dir %{python2_sitelib}/%{name}/config/
%dir %{python2_sitelib}/%{name}/http/
%dir %{python2_sitelib}/%{name}/messenger/
%dir %{python2_sitelib}/%{name}/messenger/outbox/

%changelog
* Wed Jun 13 2018 Edgar Fajardo <emfajard@ucsd.edu> - 1.5.2-2
- Make directory for binaries during install
- Correct order on the changelog
* Mon Jun 11 2018 Naveen Kashyap <nkashyap@ucsd.edu> - 1.4-1
- Change service name (factory-monitor -> glideinwms-factory-monitor)
* Mon Jun 11 2018 Edgar Fajardo <emfajard@ucsd.edu> - 1.3.5-1
- First rpm release
