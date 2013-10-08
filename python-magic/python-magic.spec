%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-magic
Version:        0.4.2
Release:        1%{?dist}
Summary:        File type identification using libmagic

Group:          Development/Languages
License:        GPLv2
URL:            https://github.com/ahupp/%{name}
Source0:        http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:	python-setuptools
%if 0%{?rhel} < 6
Requires:	python-ctypes
%endif

%description
This module uses ctypes to access the libmagic file type identification
library. It makes use of the local magic database and supports both 
textual and MIME-type output.

%prep
%setup -q
echo %{python_version}

%build


%install
%{__rm} -rf %{buildroot}
python setup.py install --root=%{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{python_sitelib}
%doc README


%changelog
* Thu May 05 2012 Matthew Jones <matthew@meez.com> - 1.1.0_beta3-1
- initial release
