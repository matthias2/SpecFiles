%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

Summary:    Enterprise scalable realtime graphing
Name:       graphite-web
Version:    0.9.10
Release:    1%{?dist}
Source:     https://launchpad.net/graphite/0.9/0.9.9/+download/%{name}-%{version}.tar.gz
Patch0:     %{name}-0.9.10-fhs-compliance.patch
License:    ASL 2.0 
Group:      Development/Libraries
BuildArch:  noarch
Url:        https://launchpad.net/graphite
Requires:   carbon = %{version}
Requires:   whisper = %{version}
Requires:   Django
Requires:   django-tagging
Requires:   pycairo
Requires:   python-ldap
Requires:   python-memcached
Requires:   python-twisted
Requires:   python-txamqp

%description
Frontend for Graphite. It can graph in real time and provides apis to obtain 
graphs.

%prep
%setup -n %{name}-%{version}
%patch0 -p1
sed -i -e 's|%PYTHON_SITELIB%|%{python_sitelib}|g' webapp/graphite/settings.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES #--install-data=%{_datadir}/%{name}

install -d -m 0755 $RPM_BUILD_ROOT%{_datadir}/%{name}
mv $RPM_BUILD_ROOT%{_prefix}/webapp $RPM_BUILD_ROOT%{_datadir}/%{name}

install -d -m 0755 $RPM_BUILD_ROOT%{_localstatedir}/log/graphite/webapp

install -d -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/graphite
mv $RPM_BUILD_ROOT%{python_sitelib}/graphite/local_settings.py.example \
   $RPM_BUILD_ROOT%{_sysconfdir}/graphite/local_settings.py.example

mv $RPM_BUILD_ROOT%{_prefix}/conf/*.example \
   $RPM_BUILD_ROOT%{_sysconfdir}/graphite/
rmdir $RPM_BUILD_ROOT/%{_prefix}/conf

ln -sf %{_sysconfdir}/graphite/local_settings.py \
       $RPM_BUILD_ROOT%{python_sitelib}/graphite/local_settings.py

rm -rf $RPM_BUILD_ROOT/usr/examples

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/graphite
%{_sysconfdir}/graphite/dashboard.conf.example
%{_sysconfdir}/graphite/graphTemplates.conf.example
%{_sysconfdir}/graphite/graphite.wsgi.example
%{_sysconfdir}/graphite/local_settings.py.example
%{_bindir}/build-index.sh
%{_bindir}/run-graphite-devel-server.py
%{_datadir}/%{name}
%{python_sitelib}/graphite
%{python_sitelib}/graphite_web-%{version}-py%{pyver}.egg-info
%attr(0755,graphite,graphite) %dir %{_localstatedir}/log/graphite
%attr(0755,graphite,graphite) %dir %{_localstatedir}/log/graphite/webapp
%attr(0755,root,root) %{python_sitelib}/graphite/manage.py
%attr(0755,root,root) %{python_sitelib}/graphite/thirdparty/pytz/tzfile.py

%changelog
* Wed May 23 2012 Aditya Patawari <adimania@fedoraproject.org> - 0.9.9-1
- Initial Build
