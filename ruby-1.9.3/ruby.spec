%define debug_package %{nil}

%global major_version 1
%global minor_version 9
%global teeny_version 3
%global patch_level 448

%global major_minor_version %{major_version}.%{minor_version}

%global ruby_version %{major_minor_version}.%{teeny_version}
%global ruby_abi %{major_minor_version}.1

%global ruby_archive %{name}-%{ruby_version}-p%{patch_level}

Name:		ruby
Version:	%{ruby_version}.%{patch_level}
Release:	1%{?dist}
Summary:	An interpreter of object-oriented scripting language
Group:		Development/Languages
License:	Ruby or BSD
URL:		http://ruby-lang.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:	ftp://ftp.ruby-lang.org/pub/%{name}/%{major_minor_version}/%{ruby_archive}.tar.bz2
Patch0:		ruby-1.9.1-p378-fix-mkmf-have_devel.patch
Patch1:		ruby-1.9.3-no-rubygems.patch
BuildRequires:	gdbm-devel
BuildRequires:	ncurses-devel
BuildRequires:	db4-devel
BuildRequires:	libffi-devel
BuildRequires:	openssl-devel
BuildRequires:	libyaml-devel
BuildRequires:	readline readline-devel
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
BuildRequires:	libX11-devel
BuildRequires:	doxygen
Requires:	%{name}-libs = %{version}-%{release}

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.

%package libs
Summary:	Libraries necessary to run Ruby
Group:		Development/Libraries
# ext/bigdecimal/bigdecimal.{c,h} are under (GPL+ or Artistic) which
# are used for bigdecimal.so
License:	(Ruby or GPLv2) and (GPL+ or Artistic)
Provides:	ruby(abi) = %{ruby_abi}
Provides:	libruby = %{version}-%{release}
Obsoletes:	libruby <= %{version}-%{release}

%description libs
This package includes the libruby, necessary to run Ruby.

%package devel
Summary:    A Ruby development environment
Group:      Development/Languages
Requires:   %{name} = %{version}-%{release}
Provides:   ruby(devel) = %{version}-%{release}
Provides:   ruby-devel = %{version}-%{release}
Obsoletes:  ruby-devel <= %{version}-%{release}
Obsoletes:  ruby(devel) <= %{version}-%{release}

%description devel
Header files and libraries for building an extension library for the
Ruby or an application embedding Ruby.

%package static
Summary:	Static libraries for Ruby development environment
Group:		Development/Languages
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libraries for for building a extension library for the
Ruby or an application embedded Ruby.

%package tcltk
Summary:	Tcl/Tk interface for scripting language Ruby
Group:		Development/Languages
# Many files under ext/tk/sample/ are under TCL
License:	(Ruby or GPLv2) and TCL
Requires:	%{name}-libs = %{version}-%{release}

%description tcltk
Tcl/Tk interface for the object-oriented scripting language Ruby.

%package irb
Summary:	The Interactive Ruby
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Provides:	irb = %{version}-%{release}
Obsoletes:	irb <= %{version}-%{release}

%description irb
The irb is acronym for Interactive Ruby.  It evaluates ruby expression
from the terminal.

%package rdoc
Summary:	A tool to generate documentation from Ruby source files
Group:		Development/Languages
# generators/template/html/html.rb is under CC-BY
License:	(GPLv2 or Ruby) and CC-BY
Requires:	%{name}-irb = %{version}-%{release}
Provides:	rdoc = %{version}-%{release}
Obsoletes:	rdoc <= %{version}-%{release}

%description rdoc
The rdoc is a tool to generate the documentation from Ruby source files.
It supports some output formats, like HTML, Ruby interactive reference (ri),
XML and Windows Help file (chm).

%package ri
Summary:	Ruby interactive reference
Group:		Documentation
Requires:	%{name}-rdoc = %{version}-%{release}
Provides:	ri = %{version}-%{release}
Obsoletes:	ri <= %{version}-%{release}

%description ri
ri is a command line tool that displays descriptions of built-in
Ruby methods, classes and modules. For methods, it shows you the calling
sequence and a description. For classes and modules, it shows a synopsis
along with a list of the methods the class or module implements.

%package docs
Summary:    HTML files for using Ruby
Group:      Development/Languages
Requires:   %{name} = %{version}-%{release}
Provides:   ruby(docs) = %{ruby_version}-%{release}
Obsoletes:  ruby-docs <= %{ruby_version}-%{release}
BuildArch:  noarch

%description docs
HTML files on the usage of using Ruby %{ruby_version}.

%prep
%setup -q -n %{ruby_archive}
%patch0 -p1
%patch1 -p1
# Remove rubygem stuff.  We'll package that separately.
%{__rm} -rf {bin,lib}/rake ext/json bin/gem

%build
# bug 489990
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
export CFLAGS

%configure \
        --disable-rpath \
        --enable-shared \
        --enable-pthread \
        --disable-rubygems

%{__make} %{?_smp_mflags} COPY="cp -p"


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
# Remove some files as they are supplied in other packages.
%{__rm} -rf %{buildroot}/%{_libdir}/%{name}/%{ruby_abi}/%{name}gems \
	%{buildroot}/%{_libdir}/%{name}/%{ruby_abi}/{,r}ubygems.rb \
	%{buildroot}/%{_libdir}/%{name}/%{ruby_abi}/rake.rb \
	%{buildroot}/%{_mandir}/man1/rake*

# Make sure config.h can be found for some other applications.
ln -sf ../%{_arch}-linux/%{name}/config.h \
        %{buildroot}/%{_includedir}/%{name}-%{ruby_abi}/%{name}/config.h

# Also need to include node.h and revision.h
install -m 0644 node.h %{buildroot}/%{_includedir}/%{name}-%{ruby_abi}/%{name}/node.h
install -m 0644 revision.h %{buildroot}/%{_includedir}/%{name}-%{ruby_abi}/%{name}/revision.h

%check
# make check doesn't work unless it is installed on the system.
# make check || :

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING
%lang(ja) %doc COPYING.ja
%doc ChangeLog GPL LEGAL NEWS README
%lang(ja) %doc README.ja
%doc ToDo
%doc doc/ChangeLog-*
%doc doc/NEWS-*
%{_bindir}/erb
%{_bindir}/ruby
%{_bindir}/testrb
%{_mandir}/man1/erb*
%{_mandir}/man1/ruby*
#%{_includedir}/ruby-%{ruby_abi}

%files libs
%{_libdir}/%{name}
%{_libdir}/libruby.so*
%exclude %{_libdir}/%{name}/%{ruby_abi}/rdoc
%exclude %{_libdir}/%{name}/%{ruby_abi}/rdoc.rb
%exclude %{_libdir}/%{name}/%{ruby_abi}/irb
%exclude %{_libdir}/%{name}/%{ruby_abi}/irb.rb
%exclude %{_libdir}/%{name}/%{ruby_abi}/*-tk.rb
%exclude %{_libdir}/%{name}/%{ruby_abi}/tcltk.rb
%exclude %{_libdir}/%{name}/%{ruby_abi}/tkextlib
%exclude %{_libdir}/%{name}/%{ruby_abi}/%{_arch}-linux/tcltklib.so
%exclude %{_libdir}/%{name}/%{ruby_abi}/%{_arch}-linux/tkutil.so
%exclude %{_libdir}/%{name}/%{ruby_abi}/tk*.rb
%exclude %{_libdir}/%{name}/%{ruby_abi}/tk

%files devel
%{_includedir}/%{name}-%{ruby_abi}
%{_libdir}/pkgconfig/ruby-1.9.pc

%files static
%defattr(-, root, root, -)
%{_libdir}/libruby-static.a

%files tcltk
%defattr(-, root, root, -)
%{_libdir}/%{name}/%{ruby_abi}/*-tk.rb
%{_libdir}/%{name}/%{ruby_abi}/tcltk.rb
%{_libdir}/%{name}/%{ruby_abi}/tk
%{_libdir}/%{name}/%{ruby_abi}/tk*.rb
%{_libdir}/%{name}/%{ruby_abi}/tkextlib
%{_libdir}/%{name}/%{ruby_abi}/%{_arch}-linux/tcltklib.so
%{_libdir}/%{name}/%{ruby_abi}/%{_arch}-linux/tkutil.so

%files irb
%defattr(-, root, root, -)
%{_bindir}/irb
%{_libdir}/%{name}/%{ruby_abi}/irb.rb
%{_libdir}/%{name}/%{ruby_abi}/irb
%{_mandir}/man1/irb.1*

%files rdoc
%defattr(-, root, root, -)
%{_bindir}/rdoc
%{_libdir}/%{name}/%{ruby_abi}/rdoc
%{_libdir}/%{name}/%{ruby_abi}/rdoc.rb

%files ri
%defattr(-, root, root, -)
%{_bindir}/ri
%{_datadir}/ri
%{_mandir}/man1/ri.1.*

%files docs
%{_datadir}/doc/%{name}/html

%changelog
* Thu Sep 08 2011 Matthew Jones <matthew@meez.com> 1.9.2.p290-1
- Initial release
