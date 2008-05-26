%define		subver	r3718
%define		rel		0.1
Summary:	LDAP extensions for Trac 0.10
Name:		trac-plugin-ldapplugin
Version:	0.5.1
Release:	0.%{subver}.%{rel}
License:	BSD-like
Group:		Applications/WWW
Source0:	%{name}-r3718.tar.bz2
# Source0-md5:	945bbc6b863929b22c829305634b41d5
URL:		http://trac-hacks.org/wiki/LdapPlugin
BuildRequires:	python-devel
BuildRequires:	python-setuptools >= 0.6
Requires:	python-ldap
Requires:	trac >= 0.10
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension enables to use existing LDAP groups to grant
permissions rather than defining permissions for every single user on
the system. The latest release also permits storage of permissions
(both users and groups permissions) in the LDAP directory itself
rather than in the SQL backend.

%prep
%setup -q -n %{name}-%{subver}

%build
%{__python} setup.py build
%{__python} setup.py egg_info

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING
%{py_sitescriptdir}/LdapPlugin-*.egg-info
%dir %{py_sitescriptdir}/ldapplugin
%{py_sitescriptdir}/ldapplugin/*.py[co]
