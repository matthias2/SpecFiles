%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%global debug_package %{nil}

Name:             v8
Version:          3.15.11
Release:          1%{?dist}
Summary:          JavaScript Engine
Group:            System Environment/Libraries
License:          BSD
URL:              http://code.google.com/p/v8
# No tarballs, pulled from svn
# Checkout script is Source1
# svn export http://https://v8.googlecode.com/svn/branches/3.15 v8-3.15.11
# cd v8-3.15.11 svn co http://gyp.googlecode.com/svn/trunk build/gyp
# cd .. && tar -jcf v8-15.11.tar.bz2 v8-3.15.11
Source0:          v8-%{version}.tar.bz2
ExclusiveArch:    %{ix86} x86_64 arm
BuildRequires:    python-devel

%description
V8 is Google's open source JavaScript engine. V8 is written in C++ and is used 
in Google Chrome, the open source browser from Google. V8 implements ECMAScript 
as specified in ECMA-262, 3rd edition.

%package devel
Group:      Development/Libraries
Summary:    Development headers and libraries for v8
Requires:   %{name} = %{version}-%{release}

%description devel
Development headers and libraries for v8.

%prep
%setup -q
%ifarch i386 i686
  %globale _myarch} ia32
%endif
%ifarch x86_64
  %global _myarch x64
%endif
%ifarch arm
  %global _myarch arm
%endif

%build
CFLAGS="$RPM_OPT_FLAGS" \
CXXFLAGS="$RPM_OPT_FLAGS" \
make V=1 \
  library=shared \
  werror=no \
  soname_version=%{version} \
  snapshot=no \
  hardfp=no \
  %{_myarch}.release

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
install -p include/*.h %{buildroot}%{_includedir}
install -p out/%{_myarch}.release/lib.target/libv8.so.%{version} %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_bindir}
install -p -m0755 out/%{_myarch}.release/d8 %{buildroot}%{_bindir}

pushd %{buildroot}%{_libdir}
ln -sf %{_libdir}/libv8.so.%{version} libv8.so
ln -sf %{_libdir}/libv8.so.%{version} libv8.so.%(echo %{version} | cut -d'.' -f1)
ln -sf %{_libdir}/libv8.so.%{version} libv8.so.%(echo %{version} | cut -d'.' -f1,2)
popd

mkdir -p %{buildroot}%{_includedir}/v8/extensions/experimental/
install -p src/extensions/*.h %{buildroot}%{_includedir}/v8/extensions/

chmod -x %{buildroot}%{_includedir}/v8*.h
chmod -x %{buildroot}%{_includedir}/v8/extensions/*.h

# install Python JS minifier scripts for nodejs
install -d %{buildroot}%{python_sitelib}
install -p -m0744 tools/jsmin.py %{buildroot}%{python_sitelib}/
chmod -R -x %{buildroot}%{python_sitelib}/*.py*

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE
%{_bindir}/d8
%{_libdir}/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_includedir}/v8/extensions/
%{python_sitelib}/j*.py*

%changelog
* Sun Dec 23 2012 Matthew Jones <matthew@meez.com> - 3.15.11-1
- Initial Release
