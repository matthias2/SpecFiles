%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%global pkgname cli53

Name:           python-cli53
Version:        0.3.6
Release:        1%{?dist}
Summary:        Command line script to administer the Amazon Route 53 DNS service

Group:          Development/Languages
License:        MIT
URL:            https://github.com/barnybug/%{pkgname}
Source0:        http://pypi.python.org/packages/source/p/%{pkgname}/%{pkgname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{pkgname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:	python-setuptools
%if 0%{?rhel} < 6
Requires:	python-ctypes
%endif
Requires:       python-argparse, python-dns, python-boto

%description
cli53 provides import and export from BIND format and simple command
line management of Route 53 domains.

%prep
%setup -q -n %{pkgname}-%{version}

%build

%install
%{__rm} -rf %{buildroot}
python setup.py install --root=%{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{python_sitelib}
%doc README.markdown PKG-INFO
%{_bindir}/%{pkgname}


%changelog
* Thu Jun 06 2013 Matthew Jones <matthew@meez.com> - 0.3.6-1
- Initial release
