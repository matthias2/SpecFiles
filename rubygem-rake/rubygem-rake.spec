# Generated from rake-0.7.3.gem by gem2rpm -*- rpm-spec -*-
%global	majorver	0.9.2
#%%global	preminorver	.beta.5
%global	rpmminorver	.%(echo %preminorver | sed -e 's|^\\.\\.*||')
%global	fullver	%{majorver}%{?preminorver}

%global	ruby_sitelib	%(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global	gemdir		%(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global	gemname	rake
%global	geminstdir	%{gemdir}/gems/%{gemname}-%{fullver}

%global	rubyabi	1.9.1

%global	fedorarel	1

Summary:	Ruby based make-like utility
Name:		rubygem-%{gemname}

Version:	%{majorver}
Release:	%{?preminorver:0.}%{fedorarel}%{?preminorver:%{rpmminorver}}%{?dist}
Group:		Development/Languages
License:	MIT
URL:		http://rake.rubyforge.org
Source0:	http://gems.rubyforge.org/gems/%{gemname}-%{fullver}.gem

Requires:	ruby(rubygems)
Requires:	ruby(abi) = %{rubyabi}
BuildRequires:	ruby(rubygems)
BuildRequires:	ruby(abi) = %{rubyabi}
## %%check
BuildArch:	noarch
Provides:	rubygem(%{gemname}) = %{version}-%{release}

%description
Rake is a Make-like program implemented in Ruby. Tasks and dependencies are
specified in standard Ruby syntax.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
# Directory ownership issue
Requires:	%{name} = %{version}-%{release}

%description    doc
This package contains documentation for %{name}.


%prep
%setup -q -c -T

%build
mkdir -p .%{gemdir}
gem install -V \
	--local \
	--install-dir $(pwd)/%{gemdir} \
	--bindir $(pwd)%{_bindir} \
	--force \
	--rdoc \
	%{SOURCE0}

%install
mkdir -p %{buildroot}%{gemdir}
cp -a .%{_prefix}/* %{buildroot}%{_prefix}/

# rpmlint issue
find %{buildroot}%{geminstdir}/{lib,test} -type f | \
	xargs sed -i -e '\@^#!/usr.*ruby@d'
find %{buildroot}%{geminstdir}/{doc,lib,test} -type f | xargs chmod 0644

# cleanup
rm %{buildroot}%{geminstdir}/.gemtest
rm -f %{buildroot}%{geminstdir}/RRR

%check

%files
%defattr(-,root,root,-)
%{_bindir}/rake
%dir	%{geminstdir}
%doc	%{geminstdir}/README.rdoc
%doc	%{geminstdir}/MIT-LICENSE
%doc	%{geminstdir}/TODO
%doc	%{geminstdir}/CHANGES
%{geminstdir}/bin
%{geminstdir}/lib
%{gemdir}/cache/%{gemname}-%{fullver}.gem
%{gemdir}/specifications/%{gemname}-%{fullver}.gemspec

%files	doc
%defattr(-,root,root,-)
%{geminstdir}/Rakefile
%{geminstdir}/install.rb
%{geminstdir}/doc
%{geminstdir}/test/
%{gemdir}/doc/%{gemname}-%{fullver}/


%changelog
* Sat Jun 11 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.2-1
- 0.9.2

* Sun Jun  5 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.1-2
- Add BR: rubygem(minitest) for %%check

* Sat Jun  4 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.1-1
- 0.9.1

* Thu Mar 18 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.0-0.4.beta.5
- 0.9.0 beta.5

* Mon Mar  7 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.0-0.3.beta.4
- 0.9.0 beta.4

* Fri Mar  4 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.0-0.2.beta.1
- 0.9.0 beta.1

* Thu Feb 24 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.0-0.1.beta.0
- 0.9.0 beta.0
- Split out document files

* Thu Feb 10 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.7-4
- Use BuildRequires, not BuildRequires(check)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.8.7-1
- 0.8.7
- Enable %%check

* Tue Mar 17 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.8.4-1
- New upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 27 2008 David Lutterkort <lutter@redhat.com> - 0.8.3-1
- Cleanup multiply listed files
- Set permissions in doc/, lib/ and test/ to 644

* Thu May 15 2008 Alan Pevec <apevec@redhat.com> 0.8.1-2
- fix shebang in scripts

* Thu May 15 2008 Alan Pevec <apevec@redhat.com> 0.8.1-1
- new upstream version

* Thu Aug 23 2007 David Lutterkort <dlutter@redhat.com> - 0.7.3-2
- Fix license tag
- Remove bogus shebangs in lib/ and test/

* Mon Jun 18 2007 David Lutterkort <dlutter@redhat.com> - 0.7.3-1
- Initial package
