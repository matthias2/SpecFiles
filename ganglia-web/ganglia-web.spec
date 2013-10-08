Summary:	Ganglia Web Frontend
Name:		ganglia-web
Version:	3.5.10
URL:		http://ganglia.info
Release:	1%{?dist}
License:	BSD
Vendor:		Ganglia Development Team <ganglia-developers@lists.sourceforge.net>
Group:		System Environment/Base
Source:		%{name}-%{version}.tar.gz
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot
Obsoletes:	ganglia-webfrontend, gweb
Requires:	php >= 5, php-gd
%if 0%{?suse_version}
%define web_prefixdir /srv/www/htdocs/ganglia
%else
%define web_prefixdir %{custom_web_prefixdir}
%endif

%{!?custom_web_prefixdir: %define web_prefixdir /var/www/html/ganglia}

Prefix: %{web_prefixdir}
BuildArchitectures: noarch

%description
This package provides a web frontend to display the XML tree published by
ganglia, and to provide historical graphs of collected metrics. This website is
written in the PHP5 language and uses the Dwoo templating engine.

%prep
%setup -q -n %{name}-%{version}

%build

%install
# Flush any old RPM build root
%__rm -rf $RPM_BUILD_ROOT

%__mkdir -p $RPM_BUILD_ROOT/%{web_prefixdir}
%__cp -rf * $RPM_BUILD_ROOT/%{web_prefixdir}
%__rm -rf $RPM_BUILD_ROOT/%{web_prefixdir}/conf
%__rm -rf $RPM_BUILD_ROOT/%{web_prefixdir}/debian
%__rm -rf $RPM_BUILD_ROOT/%{web_prefixdir}/%{name}
%__rm -f $RPM_BUILD_ROOT/%{web_prefixdir}/{*.in,*.spec,Makefile}
%__install -d -m 0755 $RPM_BUILD_ROOT/var/lib/ganglia/filters
%__install -d -m 0755 $RPM_BUILD_ROOT/var/lib/ganglia/conf
%__cp -rf conf/* $RPM_BUILD_ROOT/var/lib/ganglia/conf
%__install -d -m 0755 $RPM_BUILD_ROOT/var/lib/ganglia/dwoo
%__install -d -m 0755 $RPM_BUILD_ROOT/var/lib/ganglia/dwoo/compiled
%__install -d -m 0755 $RPM_BUILD_ROOT/var/lib/ganglia/dwoo/cache

%files
%defattr(-,root,root)
%attr(0755,nobody,nobody)/var/lib/ganglia/filters
%attr(0755,nobody,nobody)/var/lib/ganglia/conf
%attr(0755,nobody,nobody)/var/lib/ganglia/dwoo
%attr(0755,nobody,nobody)/var/lib/ganglia/dwoo/compiled
%attr(0755,nobody,nobody)/var/lib/ganglia/dwoo/cache
%{web_prefixdir}/*
/var/lib/ganglia/conf/*
%config(noreplace) %{web_prefixdir}/conf_default.php

%clean
%__rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Jul 10 2012 Matthew Jones <matthew@meez.com> - 3.5.0-1
- Updated version
- Changed name from gweb to ganglia-web
* Thu Mar 17 2011 Bernard Li <bernard@vanhpc.org>
- Renamed conf.php -> conf_default.php
* Fri Dec 17 2010 Bernard Li <bernard@vanhpc.org>
- Spec file for gweb which is split from ganglia-web subpackage
