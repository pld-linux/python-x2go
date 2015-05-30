#
# Conditional build:
%bcond_without	doc		# don't build doc
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module

%define 	module	x2go
Summary:	Python module providing X2Go client API
Name:		python-%{module}
Version:	0.5.0.3
Release:	1
License:	AGPLv3+
Group:		Development/Languages
Source0:	http://code.x2go.org/releases/source/python-%{module}/%{name}-%{version}.tar.gz
# Source0-md5:	b5359cd80779b5e50586f6dbf35fd659
Patch0:		python-x2go-py3.patch
URL:		http://www.x2go.org/
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
%if %{with python3}
BuildRequires:	python3-devel
# For 2to3
BuildRequires:	python-tools
%endif
%if %{with doc}
# For doc build
BuildRequires:	epydoc
BuildRequires:	python-gevent
BuildRequires:	python-paramiko
BuildRequires:	python-requests
BuildRequires:	python-simplejson
# For docs
BuildRequires:	python-Xlib
%endif
# for nxproxy
Requires:	nx
Requires:	python-Xlib
Requires:	python-gevent
Requires:	python-paramiko
Requires:	python-requests
Requires:	python-simplejson
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
X2Go is a server based computing environment with:
- session resuming
- low bandwidth support
- session brokerage support
- client side mass storage mounting support
- audio support
- authentication by smartcard and USB stick

This Python module allows you to integrate X2Go client support into
your Python applications by providing a Python-based X2Go client API.

%package doc
Summary:	Python X2Go client API documentation
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
This package contains the Python X2Go client API documentation.

%package -n python3-%{module}
Summary:	Python module providing X2Go client API
Group:		Development/Languages

%description -n python3-%{module}
X2Go is a server based computing environment with:
   - session resuming
   - low bandwidth support
   - session brokerage support
   - client side mass storage mounting support
   - audio support
   - authentication by smartcard and USB stick

This Python module allows you to integrate X2Go client support into
your Python applications by providing a Python-based X2Go client API.

%prep
%setup -q

%if %{with python3}
rm -rf py3
cp -a . py3
%endif

%build
%{__python} setup.py build

%if %{with python3}
cd py3
2to3 --write --nobackups py3
%{__python3} setup.py build
cd ..
%endif

%if %{with doc}
# Build the docs
mkdir -p epydoc/html
epydoc --debug -n "Python X2Go" -u http://www.x2go.org -v --html --no-private -o epydoc/html x2go/
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python3}
cd py3
%{__python3} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
cd ..
%endif

%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/x2go/tests

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README* TODO
%{py_sitescriptdir}/x2go
%{py_sitescriptdir}/x2go-%{version}-py*.egg-info

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc epydoc/html/*
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%endif
