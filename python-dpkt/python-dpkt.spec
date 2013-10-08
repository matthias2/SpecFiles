%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global oname  dpkt

Name:          python-dpkt
Version:       1.7
Release:       1%{?dist}
Summary:       Declarative command-line argument parser for python
License:       BSD
Group:         Development/Languages
URL:           https://code.google.com/p/dpkt/
Source0:       https://dpkt.googlecode.com/files/%{oname}-%{version}.tar.gz
BuildRequires: epydoc
Requires:      python
BuildArch:     noarch
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description

Python packet creation / parsing library

%package docs
Summary:    HTML files for using %{name}
Group:      Development/Languages
Requires:   %{name} = %{version}-%{release}
BuildArch:  noarch

%description docs

Example documentation for python-dpkt.

%prep
%setup -q -n %{oname}-%{version}

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}
make -j1 doc

%check

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{python_sitelib}/*
%doc AUTHORS CHANGES HACKING LICENSE README

%files docs
%doc doc

%changelog
* Mon Apr 01 2013 Matthew Jones <matthew@meez.com> - 1.7-1
- Initial release
