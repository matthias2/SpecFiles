%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global oname  dargparse

Name:          python-dargparse
Version:       0.2.1
Release:       1%{?dist}
Summary:       Declarative command-line argument parser for python
License:       MIT
Group:         Development/Languages
URL:           https://github.com/objectlabs/dargparse
# Source was generated from a github pull
Source0:       %{oname}-%{version}.tar.gz
BuildRequires: python-distribute
Requires:      python
Requires:      python-argparse
BuildArch:     noarch
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description

Declarative command-line argument parser for python

%prep
%setup -q -n %{oname}-%{version}

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

%check

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{python_sitelib}/*

%changelog
* Thu Nov 01 2012 Mathew Jones <matthew@meez.com> - 0.2.1-1
- updated to version 0.2.1 on CentOS 6.x

* Wed Jun 27 2012 Matthew Jones <matthew@meez.com> - 0.1.0-1
- Initial release
