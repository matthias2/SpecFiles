%define     groovy_root_dir /usr/share

Name:           groovy
Version:        2.0.6
Release:        1%{?dist}
License:        See: http://groovy.codehaus.org/license.html
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Group:          Development/Languages/Groovy
Summary:        Contains the base system for executing groovy scripts.
Source:         http://dist.codehaus.org/groovy/distributions/%{name}-binary-%{version}.zip
BuildArch:      noarch
BuildRequires:  unzip
Packager:       Federico Pedemonte <pedemonte@linux.it>

%description
Groovy is an object-oriented programming language for the Java Platform as an 
alternative to the Java programming language. It can be viewed as a scripting 
language for the Java Platform, as it has features similar to those of Python, 
Ruby, Perl, and Smalltalk. In some contexts, the name JSR 241 is used as an 
alternate identifier for the Groovy language.

%prep
%setup -n %{name}-%{version}
rm bin/*.bat

%build


%install
install -d $RPM_BUILD_ROOT/%{groovy_root_dir}/groovy/lib
install -p lib/* $RPM_BUILD_ROOT/%{groovy_root_dir}/groovy/lib

install -d $RPM_BUILD_ROOT/%{groovy_root_dir}/groovy/conf
install -p conf/* $RPM_BUILD_ROOT/%{groovy_root_dir}/groovy/conf

install -d $RPM_BUILD_ROOT/%{groovy_root_dir}/groovy/embeddable
install -p embeddable/* $RPM_BUILD_ROOT/%{groovy_root_dir}/groovy/embeddable

install -d $RPM_BUILD_ROOT/usr/bin
install -p bin/* $RPM_BUILD_ROOT/usr/bin

install -d $RPM_BUILD_ROOT/etc/profile.d
echo "export GROOVY_HOME=%{groovy_root_dir}/%{name}" >$RPM_BUILD_ROOT/etc/profile.d/groovy.sh
echo "setenv GROOVY_HOME %{groovy_root_dir}/%{name}" >$RPM_BUILD_ROOT/etc/profile.d/groovy.csh

%clean
rm -rf "$RPM_BUILD_ROOT"

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
/etc/profile.d/*
/usr/*

%changelog
* Sat Feb 20 2010 Federico Pedemonte <pedemonte@linux.it>
- Updated to Groovy version 1.7.1

* Sat Oct 03 2009 Federico Pedemonte <pedemonte@linux.it>
- Updated to Groovy version 1.6.5
- Removed hard-coded path/version number from spec file

* Thu Sep 10 2009 Federico Pedemonte <pedemonte@linux.it>
- Updated to Groovy version 1.6.4
- Removed hard-coded path/version number from spec file

* Sun May 17 2009 Federico Pedemonte <pedemonte@linux.it>
- Updated to Groovy version 1.6.3

* Wed Apr 29 2009 Federico Pedemonte <pedemonte@linux.it>
- Updated to Groovy version 1.6.2

* Wed Apr 08 2009 Federico Pedemonte <pedemonte@linux.it>
- Updated to Groovy version 1.6.1

* Wed Feb 18 2009 Federico Pedemonte <pedemonte@linux.it>
- Updated to Groovy version 1.6
