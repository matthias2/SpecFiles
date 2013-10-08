%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

Summary:       Fixed size round-robin style database
Name:          whisper
Version:       0.9.10
Release:       1%{?dist}
Source:        https://launchpad.net/graphite/0.9/0.9.9/+download/%{name}-%{version}.tar.gz
License:       ASL 2.0 
Group:         Development/Libraries
BuildArch:     noarch
URL:           https://launchpad.net/graphite
BuildRequires: python(abi) >= 2.6
Requires:      python(abi) >= 2.6
Provides:      python(whisper) = %{version}

%description
Fixed size round-robin style database

%prep
%setup -q -n %{name}-%{version}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root=$RPM_BUILD_ROOT

install -d -m 0755 $RPM_BUILD_ROOT%{_localstatedir}/lib/graphite/storage/whisper

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/rrd2whisper.py
%{_bindir}/whisper-create.py
%{_bindir}/whisper-fetch.py
%{_bindir}/whisper-info.py
%{_bindir}/whisper-resize.py
%{_bindir}/whisper-set-aggregation-method.py
%{_bindir}/whisper-update.py
%{_bindir}/whisper-dump.py
%{_bindir}/whisper-merge.py
%{python_sitelib}/%{name}-%{version}-py%{pyver}.egg-info
%{python_sitelib}/%{name}.py
%{python_sitelib}/%{name}.pyc
%{python_sitelib}/%{name}.pyo
%attr(0755,graphite,graphite) %dir %{_localstatedir}/lib/graphite
%attr(0755,graphite,graphite) %dir %{_localstatedir}/lib/graphite/storage
%attr(0755,graphite,graphite) %dir %{_localstatedir}/lib/graphite/storage/whisper

%changelog
* Wed May 23 2012 Aditya Patawari <adimania@fedoraproject.org> - 0.9.9-1
- Initial package
