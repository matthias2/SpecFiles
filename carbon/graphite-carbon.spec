%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

Summary:    Backend data caching and persistence daemon for Graphite
Name:       carbon
Version:    0.9.10
Release:    1%{?dist}
Source0:    https://launchpad.net/graphite/0.9/0.9.9/+download/%{name}-%{version}.tar.gz
Source1:    carbon-cache.init
Source2:    carbon-relay.init
Source3:    carbon-aggregator.init
Patch0:     %{name}-0.9.10-fhs-compliance.patch
License:    ASL 2.0
Group:      Development/Libraries
BuildArch:  noarch
URL:        https://launchpad.net/graphite
Requires:   python-twisted
Requires:   python-txamqp
Requires:   python-zope-interface

%description
Data collection agents connect to carbon and send their data, and carbon's job
is to make that data available for real-time graphing immediately and try to
get it stored on disk as fast as possible.

%prep
%setup -n %{name}-%{version}
%patch0 -p1

%build
%{__python} setup.py build

%install
%{__python} setup.py install --root=%{buildroot}

install -d -m 0755 %{buildroot}%{_sysconfdir}
install -d -m 0755 %{buildroot}%{_initrddir}
install -d -m 0755 %{buildroot}%{_localstatedir}/log/graphite/carbon-cache
install -d -m 0755 %{buildroot}%{_localstatedir}/run/graphite

mv %{buildroot}%{_prefix}/conf %{buildroot}%{_sysconfdir}/graphite
install -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/carbon-cache
install -m 0755 %{SOURCE2} %{buildroot}%{_initrddir}/carbon-relay
install -m 0755 %{SOURCE3} %{buildroot}%{_initrddir}/carbon-aggregator

find %{buildroot} -type f -name \*~\* -exec rm {} +

%clean
rm -rf %{buildroot}

%pre
getent group graphite >/dev/null || groupadd -r graphite
getent passwd graphite >/dev/null || \
    useradd -r -g graphite -d '/etc/graphite' -s /sbin/nologin \
    -c "Graphite Service User" uwsgi

%post
for svc in carbon-{aggregator,cache,relay}; do
    /sbin/chkconfig --add "$svc"
done

%preun
if [ $1 -eq 0 ]; then
    for svc in carbon-{aggregator,cache,relay}; do
        /sbin/service "$svc" stop >/dev/null 2>&1
        /sbin/chkconfig --del "$svc"
    done
fi

%postun
if [ $1 -ge 1 ]; then
    for svc in carbon-{aggregator,cache,relay}; do
        /sbin/service "$svc" condrestart >/dev/null 2>&1 || :
    done
fi

%files
%defattr(-,root,root)
%dir %attr(0755,graphite,graphite) %{_sysconfdir}/graphite
%{_initrddir}/carbon-aggregator
%{_initrddir}/carbon-cache
%{_initrddir}/carbon-relay
%{_sysconfdir}/graphite/*.example
%{_prefix}/bin/carbon-aggregator.py
%{_prefix}/bin/carbon-cache.py
%{_prefix}/bin/carbon-client.py
%{_prefix}/bin/carbon-relay.py
%{_prefix}/bin/validate-storage-schemas.py
%{python_sitelib}/%{name}-%{version}-py%{pyver}.egg-info
%{python_sitelib}/%{name}/*
%attr(0755,graphite,graphite) %{_localstatedir}/log/graphite/carbon-cache
%attr(0755,graphite,graphite) %{_localstatedir}/run/graphite
%{python_sitelib}/twisted/plugins/carbon*

%changelog
* Wed May 23 2012 Aditya Patawari <adimania@fedoraproject.org> - 0.9.9-1
- Initial Build
