%define		subver	r3718
%define		rel		0.4
Summary:	LDAP extensions for Trac 0.10
Name:		trac-plugin-ldapplugin
Version:	0.5.1
Release:	0.%{subver}.%{rel}
License:	BSD-like
Group:		Applications/WWW
Source0:	%{name}-r3718.tar.bz2
# Source0-md5:	945bbc6b863929b22c829305634b41d5
Source1:	http://trac-hacks.org/attachment/ticket/1431/trac.schema?format=raw
# Source1-md5:	11ddf867bcfa7481dcd23fad77118ff0
URL:		http://trac-hacks.org/wiki/LdapPlugin
BuildRequires:	python-devel
BuildRequires:	python-setuptools >= 0.6
Requires:	python-ldap
Requires:	trac >= 0.10
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		schemadir	/usr/share/openldap/schema

%description
This extension enables to use existing LDAP groups to grant
permissions rather than defining permissions for every single user on
the system. The latest release also permits storage of permissions
(both users and groups permissions) in the LDAP directory itself
rather than in the SQL backend.

%package -n openldap-schema-trac
Summary:	Trac LDAP schema
Group:		Networking/Daemons
Requires(post,postun):	sed >= 4.0
Requires:	openldap-servers

%description -n openldap-schema-trac
This package contains trac.schema for openldap.

%prep
%setup -q -n %{name}-%{subver}
cp -a %{SOURCE1} trac.schema

%build
%{__python} setup.py build
%{__python} setup.py egg_info

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{schemadir}
cp -a trac.schema $RPM_BUILD_ROOT%{schemadir}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post -n openldap-schema-trac
# dependant schemas: dyngroup, core (for dyngroup)
%openldap_schema_register %{schemadir}/trac.schema -d dyngroup,core
%service -q ldap restart

%postun -n openldap-schema-trac
if [ "$1" = "0" ]; then
	%openldap_schema_unregister %{schemadir}/trac.schema
	%service -q ldap restart
fi

%files
%defattr(644,root,root,755)
%doc COPYING
%{py_sitescriptdir}/LdapPlugin-*.egg-info
%dir %{py_sitescriptdir}/ldapplugin
%{py_sitescriptdir}/ldapplugin/*.py[co]

%files -n openldap-schema-trac
%defattr(644,root,root,755)
%{schemadir}/*.schema
