%define debug_package %{nil}

Name: siege
Version: 3.0.0
Release: 1%{?dist}
Summary: An http load testing and benchmarking utility
Group: Applications/System
License: GPLv2
URL: http://www.joedog.org/siege-home/
Source0: http://www.joedog.org/pub/siege/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: openssl
BuildRequires: openssl-devel

%description
Siege is an http load testing and benchmarking utility. It
was designed to let web developers measure their code under
duress, to see how it will stand up to load on the internet.
Siege supports basic authentication, cookies, HTTP and HTTPS
protocols. It lets its user hit a web server with a configurable
number of simulated web browsers. Those browsers place the
server “under siege.”

%prep

%setup -q
%{configure} \
  --prefix=%{_prefix} \
  --libdir=%{_libdir} \
  --sysconfdir=%{_sysconfdir}/%{name}

%build
%{__make} %{?_smp_flags}

%install
rm -rf %{buildroot}
%{__mkdir_p} %{buildroot}/%{_sysconfdir}/%{name}
%{__make} install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/%{name}/%{name}rc
%config(noreplace) %{_sysconfdir}/%{name}/urls.txt
%{_mandir}/man?/*

%changelog
* Thu Mar 11 2013 Matthew Jones <matthew@meez.com> - 3.0.0-1
- Initial release.
