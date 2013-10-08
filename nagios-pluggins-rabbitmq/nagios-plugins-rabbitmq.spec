%define debug_package %{nil}

Name:           nagios-plugins-rabbitmq
Version:        1.0.5
Release:        1%{?dist}
Summary:        Nagios checks for RabbitMQ

Group:          Applications/System
License:        ASL 2.0
URL:            http://github.com/jamesc/nagios-plugins-rabbitmq
Source0:        nagios-plugins-rabbitmq-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Correct for lots of packages, other common choices include eg. Module::Build
BuildRequires:  perl(Module::Build)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(JSON)
Requires:       perl(Nagios::Plugin)
Requires:       perl(LWP::UserAgent)
Requires:       perl(Getopt::Long)
Requires:       perl(Pod::Usage)

%{?perl_default_filter}

%description
Nagios checks for RabbitMQ messaging server.

These use the RabbitMQ management interface for gathering various
information about the server


%prep
%setup -q


%build
%{__perl} Build.PL --installdirs=vendor
./Build


%install
rm -rf $RPM_BUILD_ROOT
./Build pure_install --destdir=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/nagios/plugins
mv $RPM_BUILD_ROOT/%{_bindir}/* $RPM_BUILD_ROOT/%{_libdir}/nagios/plugins/
rm -rf $RPM_BUILD_ROOT/%{_bindir}
%{_fixperms} $RPM_BUILD_ROOT/*


%check
./Build test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.md
%{_libdir}/nagios/plugins/*
%{_mandir}/man1/*.1*


%changelog
* Wed Jun 19 2013 Matthew Jones <matthew@meez.com> 1.0.5-1
- added check_rabbitmq_watermark
* Wed Oct 26 2011 James Casey <jamesc.000@gmail.com> 1.0.4-1
- added check_rabbitmq_queue
* Wed Sep 07 2011 James Casey <jamesc.000@gmail.com> 1.0.3-1
- Added extra Basic Auth domain for rabbitmq 2.6.0
  Thanks to Bill Gerrard for spotting it
* Mon Jun 06 2011 James Casey <jamesc.000@gmail.com> 1.0.2-1
- Build fixes
* Wed Jan 12 2011 James Casey <jamesc.000@gmail.com> 1.0.1-1
- Add more checks
* Sun Jan 09 2011 James Casey <jamesc.000@gmail.com> 1.0.0-1
- Initial version

