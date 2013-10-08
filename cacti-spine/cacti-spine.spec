%define debug_package %{nil}

Name: cacti-spine
Version: 0.8.8a
Release: 1%{?dist}
Summary: A backend data gatherer for cacti

Group:		Applications/System
# There's a lot of stuff in there. It's all compatible.
License:	GPLv2 and LGPLv2
URL:		http://www.cacti.net/
Source0:	http://www.cacti.net/downloads/%{name}-%{version}.tar.gz
#Source1:	cacti-spine.conf

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	net-snmp-devel, mysql-devel, openssl-devel
Requires:	cacti

%description
A backend data gatherer for cacti.

%prep
%setup -q
%configure \
  --prefix=%{_prefix} \
  --sysconfdir=%{_sysconfdir}/cacti \
  --enable-lcap \
  --enable-threadsafe-gethostbyname

%build
%{__make} %{?_smp_flags}

%install
rm -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
# Rename conf file
mv %{buildroot}/%{_sysconfdir}/cacti/spine.conf.dist \
  %{buildroot}/%{_sysconfdir}/cacti/spine.conf

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ChangeLog README
%{_bindir}/spine
%{_sysconfdir}/cacti/spine.conf

%changelog
* Tue Apr 24 2011 Matthew Jones <matthew@meez.com> - 0.8.8-1
- Initial Release
