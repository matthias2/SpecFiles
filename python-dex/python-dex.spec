%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global oname  Dex

Name:          python-dex
Version:       0.5.1
Release:       1%{?dist}
Summary:       Compares MongoDB log files and index entries to make index recommendations
License:       MIT
Group:         Development/Languages
URL:           http://pypi.python.org/pypi/Dex
Source0:       http://pypi.python.org/packages/source/D/%{oname}/%{oname}-%{version}.tar.gz
BuildRequires: python
BuildRequires: PyYAML
BuildRequires: pymongo
Requires:      python
Requires:      python-argparse
Requires:      python-dargparse
Requires:      pymongo
Requires:      PyYAML
Requires:      python-ordereddict
BuildArch:     noarch
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description

Compares MongoDB log files and index entries to make index recommendations

%prep
%setup -q -n %{oname}-%{version}
# Create LICENSE
%{__cat} bin/dex | head -24 | tail -20 | %{__sed} -e 's|^# ||' -e s'|^#||' > LICENSE

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

%check
#pushd dex/test
#PYTHONPATH=../../ %{__python} test.py

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc PKG-INFO LICENSE
%{python_sitelib}/*
%{_bindir}/*

%changelog
* Sun Dec 16 2012 Matthew Jones <matthew@meez.com> - 0.5.1-1
- Updated to version 0.5.1
- Added python-ordereddict as a dependency

* Thu Nov 01 2012 Matthew Jones <matthew@meez.com> - 0.5.0-1
- Initial release for CentOS 6.x

* Wed Jun 27 2012 Matthew Jones <matthew@meez.com> - 0.2.1-1
- Initial release
