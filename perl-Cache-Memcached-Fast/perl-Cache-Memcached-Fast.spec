#
# spec file for package perl-Cache-Memcached-Fast
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

%define modname	      Cache-Memcached-Fast
%define perl_version  %(eval "`%{__perl} -V:version`"; echo $version)
%define debug_package %{nil}

Name:           perl-Cache-Memcached-Fast
Version:        0.21
Release:        1%{?dist}
Url:            http://search.cpan.org/~kroki/Cache-Memcached-Fast-%{version}
Summary:        Cache::Memcached::Fast - Perl client for memcached, in C language
BuildRequires:  perl, perl-Test-Pod-Coverage
BuildRequires:  memcached
License:        GPL/Artistic
Group:          Development/Libraries/Perl
Source:         http://search.cpan.org/CPAN/authors/id/K/KR/KROKI/%{modname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Cache::Memcached::Fast is a Perl client for memcached, a memory cache
daemon (http://www.danga.com/memcached/). Module core is implemented
in C and tries hard to minimize number of system calls and to avoid any
key/value copying for speed. As a result, it has very low CPU consumption.
API is largely compatible with Cache::Memcached, original pure Perl client,
most users of the original module may start using this module by installing
it and adding "::Fast" to the old name in their scripts (see "Compatibility
with Cache::Memcached" below for full details).


%prep
%setup -q -n %{modname}-%{version}

%build
echo y | perl Makefile.PL OPTIMIZE="$RPM_OPT_FLAGS -Wall"
make

%check
make test

%install
make DESTDIR=%{buildroot} install_vendor
echo perl_vendorarch %{perl_vendorarch}
echo perl_vendorlib %{perl_vendorlib}
# Remove unneeded perl modules and remove empty directories.
for FILE in `find %{buildroot} -name .packlist -o -name Fast.bs -o -name perllocal.pod`
do
  %{__rm} -f $FILE
done
find %{buildroot} -type d -empty -delete

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc Changes README
%doc %{_mandir}/man?/*
# %{perl_vendorlib}/*
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Cache
%{perl_vendorarch}/Cache/*

%changelog
* Mon May  6 2013 Matthew Jones <matthew@meez.com> - 0.21-1
- Upgraded to version 0.21
* Wed Dec  1 2010 coolo@novell.com
- switch to perl_requires macro
* Mon Nov 29 2010 coolo@novell.com
- remove /var/adm/perl-modules
* Sun Apr 25 2010 jw@novell.com
- update from 0.12 to 0.19 as recommended by CPAN RSS Reader  " <"meissner@novell.com>"
