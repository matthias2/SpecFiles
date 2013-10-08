%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%global pkgname glacier-cmd

%define debug_package %{nil}

Summary:	A simple lightweight interface to Amazon Web Services
Name:		python-%{pkgname}
Version:	0.2dev
Release:	1%{?dist}
License:	MIT
Group:		Development/Languages
URL:		https://github.com/uskudnik/amazon-glacier-cmd-interface
Source0:	glacier-cmd-0.2dev.tar.gz
Requires:	python, python-boto, python-dateutil
Requires:	pytz, python-prettytable, python-argparse
BuildRequires:	python-devel, python-setuptools
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Command line interface for Amazon Glacier. Allows managing vaults, uploading
and downloading archives and bookkeeping of created archives.

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
%{_bindir}/*

%changelog
* Mon Mar 11 2013 Matthew Jones <matthew@meez.com> - 0.2dev-1
- Initial release
