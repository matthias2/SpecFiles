%define debug_package %{nil}

Name:           python-psutil
Version:        0.4.1
Release:        1%{?dist}
Summary:        A process utilities module for Python

Group:          Development/Libraries
License:        BSD
URL:            http://sendapatch.se/projects/pylibmc/
Source0:        http://psutil.googlecode.com/files/psutil-%{version}.tar.gz     

BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
psutil is a module providing an interface for retrieving information
on all running processes and system utilization (CPU, disk, memory)
in a portable way by using Python, implementing many functionalities
offered by command line tools such as: ps, top, df, kill, free, lsof,
free, netstat, ifconfig, nice, ionice, iostato, iotop, uptime, tty.

%prep
%setup -q -n psutil-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
 
%files
%doc docs/ CREDITS HISTORY LICENSE README
%{python_sitearch}

%changelog
* Sat Mar 17 2012 Matthew Jones <matthew@meez.com> - 0.4.1-1
- Initial release
