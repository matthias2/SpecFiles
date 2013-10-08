%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define debug_package %{nil}

Summary: Python-Java bridge
Name: JPype
Version: 0.5.4.2
Release: 1%{?dist}
Source0: http://downloads.sourceforge.net/jpype/%{name}-%{version}.zip
License: ASL 2.0
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Vendor: Steve Menard <devilwolf@users.sourceforge.net>
URL: http://jpype.sourceforge.net/

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: python gcc-c++ python-devel java-1.6.0-openjdk-devel
Requires: python java-1.6.0-openjdk

%description
JPype is pyrhon module for:
 - launching JVM inside in python process: jpype.startJVM('/path/to/jvm.so')
 - referencing/invoking Java packages via JNI: jpype.JPackage('java.net')
 - eventyally passing python objects (callbacks) to Java with jpype.JProxy

%prep
%setup -q

%build
# Pyton doesn't like it when we export JAVA_HOME, so we are
# instead giving it directly to the setup.py script. :/ MRJ - 6/10/12
JAVA_HOME="/usr/java" \
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README.txt
%{python_sitearch}/_jpype.so
%{python_sitearch}/jpype/
%{python_sitearch}/jpypex/
%{python_sitearch}/%{name}-%{version}-*.egg-info

%changelog
* Sun Jun 10 2012 Matthew Jones <matthew@meez.com> - 0.5.4.2-1
- Initial release

