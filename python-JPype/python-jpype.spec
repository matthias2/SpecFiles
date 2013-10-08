%define module	JPype
%define tarname	JPype
%define name	python-%module
%define version	0.5.4.1
%define release	%mkrel 2
%define debug_package %{nil}


Summary:	Allow python programs full access to java class libraries.
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://media.djangoproject.com/releases/%{version}/%{tarname}-%{version}.zip
License:	BSD
Group:		Development/Python
Url:		http://www.djangoproject.com
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	python-setuptools, python-sphinx
%py_requires -d

%description
JPype is an effort to allow python programs full access to java
class libraries. This is achieved not through re-implementing
Python, as Jython/JPython has done, but rather through interfacing
at the native level in both Virtual Machines.

%prep
%setup -q -n %{tarname}-%{version}
sed -i 's/^\(ez_setup.use_setuptools\)/#\1/' setup.py

%build
export JAVA_HOME="/etc/alternatives/java_sdk_1.6.0"

PYTHONDONTWRITEBYTECODE= %__python setup.py build

%install
%__rm -rf %{buildroot}
PYTHONDONTWRITEBYTECODE= %__python setup.py install --root=%{buildroot}

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*


%changelog

