Name: cacti
Version: 0.8.8a
Release: 1%{?dist}
Summary: An rrd based graphing tool

Group: Applications/System
# There's a lot of stuff in there. It's all compatible.
License: GPLv2+ and LGPLv2 and (MPLv1.1 or GPLv2 or LGPLv2) and (LGPLv2 or BSD)
URL: http://www.cacti.net/
Source0: http://www.cacti.net/downloads/%{name}-%{version}.tar.gz
Source1: cacti-httpd.conf
Source2: cacti.logrotate
Source3: cacti.README.Fedora

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: php, php-mysql, mysql, httpd, rrdtool, net-snmp, net-snmp-utils, php-snmp
Requires(pre): %{_sbindir}/useradd
Requires(postun): /sbin/service 
BuildArch: noarch

%description
Cacti is a complete frontend to RRDTool. It stores all of the
necessary information to create graphs and populate them with
data in a MySQL database. The frontend is completely PHP
driven. Along with being able to maintain graphs, data
sources, and round robin archives in a database, Cacti also
handles the data gathering. There is SNMP support for those
used to creating traffic graphs with MRTG.

%prep
%setup -q

echo "#*/5 * * * *	cacti	%{_bindir}/php %{_datadir}/%{name}/poller.php > /dev/null 2>&1" >cacti.cron

%install
rm -rf %{buildroot}
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/%{name}
%{__install} -d -m 0755 %{buildroot}/%{_docdir}/%{name}-%{version}
%{__install} -d -m 0755 %{buildroot}/%{_datadir}/%{name}/
%{__install} -m 0644 *.php %{buildroot}/%{_datadir}/%{name}/
%{__install} -d -m 0775 log/ %{buildroot}/%{_localstatedir}/log/%{name}/
%{__install} -m 0664 log/* %{buildroot}/%{_localstatedir}/log/%{name}/
%{__install} -d -m 0755 rra/ %{buildroot}/%{_localstatedir}/lib/%{name}/rra/
%{__install} -d -m 0755 scripts/ %{buildroot}/%{_localstatedir}/lib//%{name}/scripts/
%{__install} -m 0755 scripts/* %{buildroot}/%{_localstatedir}/lib/%{name}/scripts/
%{__install} -d -m 0755 cli/ %{buildroot}/%{_localstatedir}/lib//%{name}/cli/
%{__install} -m 0755 cli/* %{buildroot}/%{_localstatedir}/lib/%{name}/cli/
%{__install} -d -m 0755 plugins/ %{buildroot}/%{_localstatedir}/lib/%{name}/plugins/
%{__install} -m 0644 plugins/* %{buildroot}/%{_localstatedir}/lib/%{name}/plugins/
%{__install} -D -m 0644 cacti.cron %{buildroot}/%{_sysconfdir}/cron.d/cacti
%{__install} -D -m 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/httpd/conf.d/cacti.conf
%{__install} -D -m 0644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/logrotate.d/cacti

# The su parameter will trip up older logrotate versions.
# Conditionally remove it here.
%if (0%{?fedora} && 0%{?fedora} <= 15) || (0%{?rhel} && 0%{?rhel} <= 6)
	sed -i %{buildroot}/%{_sysconfdir}/logrotate.d/cacti -e '/^[ \t]*su /d'
%endif

%{__cp} -a images/ include/ install/ lib/ resource/ %{buildroot}%{_datadir}/%{name}
%{__cp} %{SOURCE3} ./docs/README.cacti
%{__cp} -a docs/ %{buildroot}/%{_docdir}/%{name}-%{version}
%{__mv} %{buildroot}/%{_datadir}/%{name}/include/config.php %{buildroot}/%{_sysconfdir}/%{name}/db.php
%{__chmod} +x %{buildroot}/%{_datadir}/%{name}/cmd.php %{buildroot}/%{_datadir}/%{name}/poller.php
ln -s %{_sysconfdir}/%{name}/db.php %{buildroot}/%{_datadir}/%{name}/include/config.php
ln -s %{_localstatedir}/lib/%{name}/rra %{buildroot}/%{_datadir}/%{name}/
ln -s %{_localstatedir}/lib/%{name}/scripts %{buildroot}/%{_datadir}/%{name}/
ln -s %{_localstatedir}/lib/%{name}/cli %{buildroot}/%{_datadir}/%{name}/
ln -s %{_localstatedir}/lib/%{name}/plugins %{buildroot}/%{_datadir}/%{name}/
ln -s %{_localstatedir}/log/%{name}/ %{buildroot}/%{_datadir}/%{name}/log
ln -s %{_datadir}/%{name}/lib %{buildroot}/%{_localstatedir}/lib/%{name}/
ln -s %{_datadir}/%{name}/include %{buildroot}/%{_localstatedir}/lib/%{name}/

%clean
rm -rf %{buildroot}

%pre
%{_sbindir}/useradd -d %{_datadir}/%{name} -r -s /sbin/nologin cacti 2> /dev/null || :

%post
if [ $1 == 1 ]; then
	/sbin/service httpd condrestart > /dev/null 2>&1 || :
fi

%postun
/sbin/service httpd condrestart > /dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_localstatedir}/lib/%{name}
%dir %{_localstatedir}/lib/%{name}/cli
%dir %{_localstatedir}/lib/%{name}/scripts
%doc docs/ README LICENSE cacti.sql
%config(noreplace) %{_sysconfdir}/cron.d/cacti
%config(noreplace) %{_sysconfdir}/httpd/conf.d/cacti.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0640,cacti,apache) %config(noreplace) %{_sysconfdir}/%{name}/db.php
%{_datadir}/%{name}/*.php
%{_datadir}/%{name}/images/
%{_datadir}/%{name}/include/
%{_datadir}/%{name}/install/
%{_datadir}/%{name}/lib/
%{_datadir}/%{name}/log
%{_datadir}/%{name}/resource/
%{_datadir}/%{name}/rra
%{_datadir}/%{name}/scripts
%{_datadir}/%{name}/cli
%{_datadir}/%{name}/plugins
%{_localstatedir}/lib/%{name}/scripts/*[^p]
%attr(-,cacti,apache) %{_localstatedir}/log/%{name}/
%attr(-,cacti,root) %{_localstatedir}/lib/%{name}/rra/
%attr(0644,root,root) %{_localstatedir}/lib/%{name}/scripts/*php
%attr(0644,root,root) %{_localstatedir}/lib/%{name}/cli/*php
%attr(0644,root,root) %{_localstatedir}/lib/%{name}/include
%attr(0644,root,root) %{_localstatedir}/lib/%{name}/lib
%attr(0644,root,root) %{_localstatedir}/lib/%{name}/plugins

%changelog
* Tue Dec 13 2011 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.8.7i-2
- Only set "su" logrotate parameter for F16 and above.
- Tweak mod_security rules.

* Mon Dec 12 2011 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.8.7i-1
- New upstream release (BZ #766573).

* Fri Nov 11 2011 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.8.7h-2
- block HTTP access to log and rra directories (#609856)
- overrides for mod_security
- set logrotate to su to cacti apache when rotating (#753079)

* Thu Oct 27 2011 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.8.7h-1
- New upstream release.
- Remove upstream'd mysql patch.

* Mon Aug 08 2011 Jon Ciesla <limb@jcomserv.net> - 0.8.7g-3
- Patch for MySQL 5.5, BZ 728513.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.7g-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 12 2010 Mike McGrath <mmcgrath@redhat.com> 0.8.7g-1
- Upstream released new version

* Mon May 24 2010 Mike McGrath <mmcgrath@redhat.com> - 0.8.7f-1
- Upstream released new version
- Contains security updates #595289

* Fri Apr 23 2010 Mike McGrath <mmcgrath@redhat.com> - 0.8.7e-4
- Pulling in patches from upstream
- SQL injection fix
- BZ #541279

* Tue Dec  1 2009 Mike McGrath <mmcgrath@redhat.com> - 0.8.7e-3
- Pulling in some official patches
- #541279
- #541962

* Sun Aug 16 2009 Mike McGrath <mmcgrath@redhat.com> - 0.8.7e-1
- Upstream released new version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.7d-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 31 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 0.8.7d-3
- Fix unowned cli directory (#473631)

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.7d-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 21 2009 Mike McGrath <mmcgrath@redhat.com> - 0.8.7d-1
- Upstream released new version

* Mon Jul 28 2008 Mike McGrath <mmcgrath@redhat.com> - 0.8.7b-4
- Added cli directory

* Fri Jul 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.7b-3
- fix my own mistake in the license tag

* Tue Jul 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.7b-2
- fix license tag

* Thu Feb 14 2008 Mike McGrath <mmcgrath@redhat.com> - 0.8.7b-1
- Upstream released new version

* Fri Nov 23 2007 Mike McGrath <mmcgrath@redhat.com> - 0.8.7a-2
- db.php is now 640 instead of 660 - #396331

* Tue Nov 20 2007 Mike McGrath <mmcgrath@redhat.com> - 0.8.7a-1
- Upstream released new version
- Fixes for bug #391691 - CVE-2007-6035

* Fri Oct 13 2007 Mike McGrath <mmcgrath@redhat.com> - 0.8.7-2
- Upstream released new version
- No longer need to patch for /etc/cacti/*

* Fri Sep 14 2007 Mike McGrath <mmcgrath@redhat.com> - 0.8.6j-8
- Fix for CVE-2007-3112 bz#243592

* Sat Sep 08 2007 Mike McGrath <mmcgrath@redhat.com> - 0.8.6j-6
- rebuild

* Sat May 05 2007 Mike McGrath <mmcgrath@redhat.com> - 0.8.6j-5
- Upstream released new version

* Fri Jan 12 2007 Mike McGrath <imlinux@gmail.com> - 0.8.6i-5
- Added 4 upstream patches
- Fix for BZ 222410

* Thu Nov 09 2006 Mike McGrath <imlinux@gmail.com> - 0.8.6i-4
- Patch now includes <?php BG# 214914

* Thu Sep 07 2006 Mike McGrath <imlinux@gmail.com> - 0.8.6i-3
- Upstream released new version

* Thu Sep 07 2006 Mike McGrath <imlinux@gmail.com> - 0.8.6i-2
- Upstream released new version

* Thu Sep 07 2006 Mike McGrath <imlinux@gmail.com> - 0.8.6h-7
- Mass rebuild

* Wed Feb 22 2006 Mike McGrath <imlinux@gmail.com> - 0.8.6h-6
- Disabled Cron job by default

* Tue Feb 14 2006 Mike McGrath <imlinux@gmail.com> - 0.8.6h-5
- Rebuild for Fedora Extras 5

* Mon Feb 6 2006 Mike McGrath <imlinux@gmail.com> - 0.8.6h-4
- Fixed some scriptlets to always return 0
- Fixed extra '/' in logrotate
- Added README.Fedora

* Wed Jan 14 2006 Mike McGrath <imlinux@gmail.com> - 0.8.6h-3
- Fixed device filter clear issue
- Fixed invalid SQL graph generation statement
- Fixed php warning for empty set non-existant rrd file
- Added MySQL 5.x 'strict mode' compatibility

* Mon Jan 09 2006 Mike McGrath <imlinux@gmail.com> - 0.8.6h-1
- MySQL 5.x support
- IPv6 support to lib/ping.php
- Command line scripts for copying users, reindxing and rebuilding cache
- Many Bug fixes

* Tue Dec 18 2005 Mike McGrath <imlinux@gmail.com> - 0.8.6g-7
- Separated database configs from config.php
- Fixed the 'short_open_tag" syntax error
- Fixed graph zoom graph bug
- Fixed SNMP auth bug
- Re-enables MIB file parsing in poller
- Created a Fedora frendly version of the RPM

* Wed Sep 7 2005 Ian Berry <iberry@raxnet.net> - 0.8.6g-1
- Updated to release 0.8.6g.

* Mon Jul 1 2005 Ian Berry <iberry@raxnet.net> - 0.8.6f-1
- Updated to release 0.8.6f.

* Mon Jun 20 2005 Ian Berry <iberry@raxnet.net> - 0.8.6e-1
- Updated to release 0.8.6e.

* Wed Apr 26 2005 Ian Berry <iberry@raxnet.net> - 0.8.6d-1
- Updated to release 0.8.6d.

* Wed Dec 12 2004 Ian Berry <iberry@raxnet.net> - 0.8.6c-1
- Updated to release 0.8.6c.

* Wed Oct 5 2004 Ian Berry <iberry@raxnet.net> - 0.8.6b-1
- Updated to release 0.8.6b.

* Sun Oct 3 2004 Ian Berry <iberry@raxnet.net> - 0.8.6a-1
- Updated to release 0.8.6a.

* Sat Sep 11 2004 Ian Berry <iberry@raxnet.net> - 0.8.6-1
- Updated to release 0.8.6.
- Broke cactid into its own package.

* Thu Apr 4 2004 Ian Berry <iberry@raxnet.net> - 0.8.5a-1
- Initial package.

