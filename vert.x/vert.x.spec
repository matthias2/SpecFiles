Name: vert.x		
Version: 1.3.0.final
Release: 1%{?dist}
Summary: Framework for JavaScript, CoffeeScript, Ruby, Python, Groovy and Java

License: ASL 2.0
URL: http://vertx.io/	
Source0: http://vertx.io/downloads/%{name}-%{version}.tar.gz
BuildArch: noarch

#BuildRequires:	
Requires: java-1.7.0-openjdk
Requires: jython
Requires: jruby
Patch0: vert.x-1.3.0-p1.patch

%description
Vert.x is an event driven application framework that runs 
on the JVM - a run-time with real concurrency and 
unrivalled performance. Vert.x then exposes the API in 
Ruby, Java, Groovy, JavaScript and Python.
You can check examples at http://vertx.io/examples.html
or take a look at the vertx documentation at
http://vertx.io/docs.html

%prep
%setup -q 
%patch0 -p1

%install
install -d %{buildroot}%{_datadir}/vertx
install -d %{buildroot}%{_datadir}/vertx/api-docs
install -d %{buildroot}%{_datadir}/vertx/client
install -d %{buildroot}%{_datadir}/vertx/conf
install -d %{buildroot}%{_datadir}/vertx/examples
install -d %{buildroot}%{_datadir}/vertx/lib
install -d %{buildroot}%{_bindir}
install -b lib/* %{buildroot}%{_datadir}/vertx/lib
install -b conf/* %{buildroot}%{_datadir}/vertx/conf
install -b client/* %{buildroot}%{_datadir}/vertx/client
cp -r  api-docs/* %{buildroot}%{_datadir}/vertx/api-docs
cp -r examples/* %{buildroot}%{_datadir}/vertx/examples
install bin/vertx %{buildroot}%{_bindir}

%files
%dir %{_datadir}/vertx
%dir %{_datadir}/vertx/client
%dir %{_datadir}/vertx/conf
%dir %{_datadir}/vertx/lib
%dir %{_datadir}/vertx/api-docs
%dir %{_datadir}/vertx/examples
%{_bindir}/vertx
%{_datadir}/vertx/client/*
%{_datadir}/vertx/conf/*
%{_datadir}/vertx/lib/*
%{_datadir}/vertx/api-docs/*
%{_datadir}/vertx/examples/*

%changelog
* Mon Jan 07 2013 Matias Kreder <delete@fedoraproject.org> 1.3.0.final-1
- Initial release.

