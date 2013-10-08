%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%global pkgname mrjob

%define debug_package %{nil}

Summary:	A simple lightweight interface to Amazon Web Services
Name:		python-mrjob
Version:	0.3.5
Release:	1%{?dist}
License:	Apache License, Version 2.0
Group:		Development/Languages
URL:		https://github.com/Yelp/%{pkgname}
Source:		https://pypi.python.org/packages/source/m/%{pkgname}/%{pkgname}-%{version}.tar.gz
Requires:	python, python-simplejson, python-boto >= 2.0, PyYAML
BuildRequires:	python-devel, python-setuptools
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
mrjob fully supports Amazon's Elastic MapReduce (EMR) service, which allows you
to buy time on a Hadoop cluster on an hourly basis. It also works with your own
Hadoop cluster.

%prep
%setup -q -n %{pkgname}-%{version}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

%changelog
* Mon Mar 11 2013 Matthew Jones <matthew@meez.com> - 0.3.5-1
- Initial release
