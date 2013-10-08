%define debug_package %{nil}
%define __jar_repack %{nil}

Name:		resin
Version:	4.0.36
Release:	1%{?dist}
Summary:	A fast Servlet and JSP engine
Group:		Networking/Daemons
URL:		http://www.caucho.com
License:	GPL2
Source0:	http://www.caucho.com/download/%{name}-%{version}.tar.gz
#Source0:	http://www.caucho.com/download/%{name}-%{version}-src.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	openssl-devel
# We are using jrockit for 64bit java support
# So we aren't going to include it as a dependency
#BuildRequires:	/usr/java
#BuildRequires:	java-1.6.0-openjdk-devel
#Requires:	java-1.6.0-openjdk
BuildRequires:	jdk
Requires:	openssl

# Get rid of perl(GZip) dependency. They are built into resin.
# Taken from openvpn.spec file.
%define __perl_requires sh -c 'cat > /dev/null'

%description
Resin is a fast JavaEE 6 web server. It is built on our distributed-agent
technology for the elastic cloud. Our administration and health monitoring
tools provide statistics, troubleshooting and application management. The
resin cloud scales messaging, caching, load balancing and deployment
services for new servers without a need for configuration.

%pre
getent group resin > /dev/null || groupadd -r resin
getent passwd resin > /dev/null || \
  useradd -r -g resin -d /dwm/dirtyclubs -s /sbin/nologin \
  -c "Resin JSP Engine" resin
exit 0

%prep
%setup -q
# Remove windows files
%{__rm} -f bin/*.bat
%{__mkdir} m4
# Java binary isn't picked up by configure.
#export PATH="/usr/java/bin:$PATH"
%{__chmod} 0755 configure
%{configure} \
	--program-prefix=%{_prefix} \
	--prefix=%{_libdir}/%{name} \
	--with-resin-root=%{_var}/www/%{name} \
	--with-resin-conf=%{_sysconfdir}/%{name} \
	--with-resin-log=%{_var}/log/%{name} \
	--with-resin-init.d=%{_sysconfdir}/rc.d/init.d/%{name}

%build
%{__make} %{?_smp_flags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
# Fix a broken symlink
%{__mkdir_p} %{buildroot}%{_bindir}
%{__ln_s} %{_libdir}/%{name}/bin/%{name}ctl %{buildroot}/%{_bindir}/%{name}ctl
# Remove *.in files.
find %{buildroot} -iname "*\.in" -exec rm -f '{}' \;

%post
/sbin/chkconfig --add resin || :

%preun
if [ "$1" = 0 ] ; then
  /sbin/service resin stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del resin || :
fi

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README LICENSE
%{_sysconfdir}/rc.d/init.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/resin.properties
%config(noreplace) %{_sysconfdir}/%{name}/resin.xml
%{_sysconfdir}/%{name}/*
%{_bindir}/%{name}ctl
%{_libdir}/%{name}
%attr(-,resin,resin) %{_var}/www/%{name}
%attr(-,resin,resin) %{_var}/log/%{name}

%changelog
* Sun Apr 21 2013 Matthew Jones <matthew@meez.com> - 4.0.35-1
- Update version

* Sat Nov 19 2011 Matthew Jones <matthew@meez.com> - 4.0.24-1
- Initial release
