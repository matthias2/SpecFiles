%global confdir       ext/redhat
%global initrddir     /etc/rc.d/init.d
# VERSION is subbed out during rake srpm process
%global realversion   1.2.23
%global rpmversion    1.2.23
%global dbuser        puppet-dashboard

Name:           puppet-dashboard
Version:        %{rpmversion}
Release:        1%{?dist}
Summary:        Systems Management web application
Group:          Applications/System
License:        ASL 2.0
Vendor:         %{?_host_vendor}
URL:            http://www.puppetlabs.com
Source0:        http://downloads.puppetlabs.com/dashboard/%{name}-%{realversion}.tar.gz
BuildArch:      noarch
#Requires:	 ruby(abi) = 1.9.1, ruby > 1.9.2
#Requires:       ruby(abi) = 1.8, ruby > 1.8.7
# Puppet-dashboard also requires rubygem(rake), rubygems and ruby-mysql.
# We'll add these via rubygems
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-%(id -un)

Requires(pre):    shadow-utils
Requires(post):   chkconfig
Requires(preun):  chkconfig
Requires(preun):  initscripts
Requires(postun): initscripts

%description
Puppet Dashboard is a systems management web application for managing
Puppet installations and is written using the Ruby on Rails framework.

%pre
getent group %{dbuser} > /dev/null || groupadd -r %{dbuser}
getent passwd %{dbuser} > /dev/null || \
  useradd -r -g %{dbuser} -d %{_datadir}/puppet-dashboard -s /sbin/nologin \
  -c "Puppet Dashboard" %{dbuser}
exit 0

%prep
%setup -q -n %{name}-%{realversion}

%build

%install
rm -rf $RPM_BUILD_ROOT

install -p -d -m0755 $RPM_BUILD_ROOT/%{_datadir}/%{name}
install -p -d -m0755 $RPM_BUILD_ROOT/%{_datadir}/%{name}/log
install -p -d -m0755 $RPM_BUILD_ROOT/%{_datadir}/%{name}/public
install -p -d -m0755 $RPM_BUILD_ROOT/%{_datadir}/%{name}/tmp
install -p -d -m0755 $RPM_BUILD_ROOT/%{_datadir}/%{name}/vendor
install -p -d -m0755 $RPM_BUILD_ROOT/%{_datadir}/%{name}/certs
install -p -d -m0755 $RPM_BUILD_ROOT/%{_defaultdocdir}/%{name}-%{version}
install -p -d -m0755 $RPM_BUILD_ROOT/%{_datadir}/%{name}/spool
install -p -d -m0755 $RPM_BUILD_ROOT/%{_datadir}/%{name}/examples
cp -p -r app bin config db ext lib public Rakefile script spec examples vendor $RPM_BUILD_ROOT/%{_datadir}/%{name}
install -Dp -m0640 config/database.yml.example $RPM_BUILD_ROOT/%{_datadir}/%{name}/config/database.yml
install -Dp -m0640 config/settings.yml.example $RPM_BUILD_ROOT/%{_datadir}/%{name}/config/settings.yml
install -Dp -m0644 VERSION $RPM_BUILD_ROOT/%{_datadir}/%{name}/VERSION
chmod a+x $RPM_BUILD_ROOT/%{_datadir}/%{name}/script/*

# Add sysconfig and init script
install -Dp -m0755 %{confdir}/%{name}.init $RPM_BUILD_ROOT/%{initrddir}/puppet-dashboard
install -Dp -m0755 %{confdir}/puppet-dashboard-workers.init $RPM_BUILD_ROOT/%{initrddir}/puppet-dashboard-workers
install -Dp -m0644 %{confdir}/%{name}.sysconfig $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/puppet-dashboard
install -Dp -m0644 %{confdir}/%{name}.logrotate $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/puppet-dashboard

# Put logs in /var/log and symlink in /usr/share (FHS work)
#mkdir -p $RPM_BUILD_ROOT/var/log/%{name}
#if $(stat $RPM_BUILD_ROOT/%{_datadir}/%{name}/log/*) ; then
#  rsync -avx $RPM_BUILD_ROOT/%{_datadir}/%{name}/log/* $RPM_BUILD_ROOT/var/log/%{name}
#fi
#rm -rf $RPM_BUILD_ROOT/%{_datadir}/%{name}/log
#ls -l $RPM_BUILD_ROOT/%{_datadir}/%{name}
#cd $RPM_BUILD_ROOT/var/log
#ln -sf %{name} ../..%{_datadir}/%{name}/log


# Clean up some rpmlint issues
find $RPM_BUILD_ROOT -iname "\.git*" -exec rm -rf '{}' \;
rm -rf $RPM_BUILD_ROOT/%{_datadir}/%{name}/ext/{redhat,debian,build_defaults.yaml,project_data.yaml}

%post

/sbin/chkconfig --add puppet-dashboard || :
/sbin/chkconfig --add puppet-dashboard-workers || :

%preun
if [ "$1" = 0 ] ; then
  /sbin/service puppet-dashboard stop > /dev/null 2>&1
  /sbin/service puppet-dashboard-workers stop > /dev/null 2>&1
  /sbin/chkconfig --del puppet-dashboard || :
  /sbin/chkconfig --del puppet-dashboard-workers || :
fi

%postun
if [ "$1" -ge 1 ]; then
  /sbin/service puppet-dashboard condrestart >/dev/null 2>&1 || :
  /sbin/service puppet-dashboard-workers condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,)
%doc LICENSE README.markdown README_PACKAGES.markdown
%attr(-,puppet-dashboard,puppet-dashboard) %config(noreplace) %{_datadir}/%{name}/config/*
%{initrddir}/puppet-dashboard
%{initrddir}/puppet-dashboard-workers
%config(noreplace) %{_sysconfdir}/sysconfig/puppet-dashboard
%config %{_sysconfdir}/logrotate.d/puppet-dashboard
%attr(-,puppet-dashboard,puppet-dashboard) %doc %{_datadir}/puppet-dashboard/VERSION
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/puppet-dashboard/Rakefile
%attr(-,puppet-dashboard,puppet-dashboard) %dir %{_datadir}/%{name}/config
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/app
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/bin
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/db
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/ext
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/lib
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/log
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/public
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/script
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/spec
%attr(-,puppet-dashboard,puppet-dashboard) %dir %{_datadir}/%{name}/spool
%attr(-,puppet-dashboard,puppet-dashboard) %dir %{_datadir}/%{name}/tmp
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/vendor
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/certs
%attr(-,puppet-dashboard,puppet-dashboard) %{_datadir}/%{name}/examples
#%attr(-,puppet-dashboard,puppet-dashboard) %dir /var/log/%{name}

%changelog
* Thu Jul 12 2012  Michael Stahnke <stahnma@puppetlabs.com> -  1.2.10-1
- Build for 1.2.10

* Mon Jul 04 2011 Michael Stahnke <stahnma@puppetlabs.com> - 1.1.9-2
- Updating spec to fix some rpmlint issues
- Began work on FHS issues, but have not completed (commented out)
- Adding a spool directory

* Thu Jun 30 2011 Michael Stahnke <stahnma@puppetlabs.com> - 1.1.9-1
- Using 1.1.9 as 1.2 alpha for upgradability reasons
- Fixing "file listed twice" warnings

* Tue May 17 2011 Michael Stahnke <stahnma@puppetlabs.com> - 1.1.1-1
- New release

* Thu Apr 07 2011 James Turnbull <james@puppetlabs.com> - 1.1.0-1
- Removed zero byte file deletion
- Incremented version

* Fri Jul 30 2010 James Turnbull <james@puppetlabs.com> - 1.0.3-3
- Fixed database.yml error

* Fri Jul 30 2010 James Turnbull <james@puppetlabs.com> - 1.0.3-2
- Fixed VERSION issue

* Thu Jul 29 2010 James Turnbull <james@puppetlabs.com> - 1.0.3-1
- Incremented version

* Sat Jul 15 2010 James Turnbull <james@puppetlabs.com> - 1.0.1-2
- Added MySQL requires
- Configured database.yml file

* Fri Jul 14 2010 James Turnbull <james@puppetlabs.com> - 1.0.1-1
- Removed rspec-rails plugin
- Removed doc files
- Updated for Puppet Labs 1.0.1 release

* Mon May 03 2010 Todd Zullinger <tmz@pobox.com> - 1.0.0-4
- Don't define %%_initrddir, rpm has defined it since the Red Hat Linux days
  (When RHEL-6 and Fedora-9 are the oldest supported releases, %%_initddir should
  be used instead.)
- %%global is preferred over %%define
  https://fedoraproject.org/wiki/Packaging:Guidelines#Source_RPM_Buildtime_Macros
- Drop use of %%{__mkdir} and similar, the macros add nothing but clutter
- Fix Source0 URL

* Mon May  3 2010 James Turnbull <james@lovedthanlost.net> - 1.0.0-3
- Fixed init script type

* Fri Apr 16 2010 James Turnbull <james@lovedthanlost.net> - 1.0.0-2
- Added init script support
- Imported changes for older RPM builds provided by Michael Stahnke

* Thu Mar 26 2010 James Turnbull <james@lovedthanlost.net> - 1.0.0-1
- Initial release.
