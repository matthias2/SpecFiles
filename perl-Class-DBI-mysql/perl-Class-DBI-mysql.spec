Name:           perl-Class-DBI-mysql
Version:        1.00
Release:        7%{?dist}
Summary:        Extensions to Class::DBI for MySQL
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Class-DBI-mysql/
Source0:        http://search.cpan.org/CPAN/authors/id/T/TM/TMTM/Class-DBI-mysql-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:	perl(Class::DBI), perl(DBD::mysql), perl(Test::More)
Requires:  perl(Class::DBI), perl(DBD::mysql), perl(Time::Piece::MySQL)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
%{summary}.

%prep
%setup -q -n Class-DBI-mysql-%{version}
perldoc -t perlartistic > Artistic
perldoc -t perlgpl > COPYING

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
# Needs a running mysql server.
#make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Artistic COPYING Changes
%{perl_vendorlib}/Class/DBI
%{_mandir}/man3/*.3*


%changelog
* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.00-5
- Rebuild for perl 5.10 (again)

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.00-4
- rebuild for new perl

* Fri Aug 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.00-3
- license fix

* Thu Sep 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.00-2
- bump for fc-6

* Mon Jan  9 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.00-1
- bump to 1.00

* Fri Sep  2 2005 Paul Howarth <paul@city-fan.org> 0.23-3
- remove redundant BR: perl
- honor %%{_smp_mflags}
- include license text
- add perl(DBD::mysql) and perl(Time::Piece::MySQL) deps

* Fri Jul  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.23-2
- cleanups

* Wed Jul  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.23-1
- Initial package for Fedora Extras
