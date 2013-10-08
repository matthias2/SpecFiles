%define debug_package %{nil}

Name:		fcgiwrap
Version:	1.1.0
Release:	1%{?dist}
Summary:	Simple FastCGI server for running CGI applications

Group:		System/Servers
License:	BSD
URL:		http://nginx.localdomain.pl/wiki/FcgiWrap
Source0:	https://github.com/downloads/gnosek/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	fcgi-devel

# Weird directory names sometimes come from github downloads.
%define fcgiwrap_dirname %(%{__tar} -tf %{S:0} | head -1)

%description
fcgiwrap  is a simple server for running CGI applications over FastCGI.
It hopes to provide clean CGI support to Nginx (and other  web  servers
that may need it).

%prep
%setup -q -n %{fcgiwrap_dirname}
autoreconf -ivf
%{configure} --prefix=""

%build
%{__make} %{?_smp_flags}

%install
rm -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.rst
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8.*

%changelog
* Tue Apr 24 2011 Matthew Jones <matthew@meez.com> - 1.0.3-1
- Initial Release
