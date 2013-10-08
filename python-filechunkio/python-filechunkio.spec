%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%global pkgname filechunkio

Summary:	Python utility to upload multiple files to Amazon S3
Name:		python-%{pkgname}
Version:	1.5
Release:	1%{?dist}
License:	MIT
Group:		Development/Languages
URL:		https://bitbucket.org/fabian/%{pkgname}
Source:		http://pypi.python.org/packages/source/f/%{pkgname}/%{pkgname}-%{version}.tar.gz
Requires:	python
BuildRequires:	python
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
FileChunkIO to upload huge files to Amazon S3 in multiple parts without
having to split them physically upfront (which requires more time and
twice the disk space) or creating in-memory chunks as StringIO instances.

%prep
%setup -q -n %{pkgname}-%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README
%{python_sitelib}/*

%changelog
* Sat May 05 2012 Matthew Jones <matthew@meez.com> - 1.5-1
- Initial Release
