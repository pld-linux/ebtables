%define		ver	2.0.10
%define		vermin	4
Summary:	Ethernet Bridge Tables
Summary(pl.UTF-8):	Ethernet Bridge Tables - filtrowanie i translacja adresów dla Ethernetu
Name:		ebtables
Version:	%{ver}.%{vermin}
Release:	2
License:	GPL
Group:		Networking/Daemons
Source0:	http://downloads.sourceforge.net/ebtables/%{name}-v%{ver}-%{vermin}.tar.gz
# Source0-md5:	506742a3d44b9925955425a659c1a8d0
Source1:	%{name}.init
Source2:	%{name}-config
Patch0:		ebtables-audit.patch
Patch1:		ebtables-linkfix.patch
Patch2:		ebtables-norootinst.patch
URL:		http://ebtables.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The ebtables project is the Linux 2.5.x (and above) Link Layer
firewalling subsystem, a patch for 2.4.x is maintained too. It
delivers for Linux the functionality of Ethernet frame filtering, all
kinds of frame NAT (Network Address Translation) and frame matching.
The ebtables infrastructure is a part of the standard Linux 2.5.x (and
above) kernels.

%description -l pl.UTF-8
Projekt ebtables to podsystem firewallingu na poziomie łącza dla
Linuksa w wersjach 2.5.x i nowszych (dostępna jest też łata do 2.4.x).
Dostarcza dla Linuksa funkcjonalność filtrowania ramek ethernetowych,
wszystkie rodzaje translacji adresów (NAT) dla ramek oraz
dopasowywanie ramek. Infrastruktura ebtables jest częścią
standardowych jąder Linuksa w wersjach 2.5.x i nowszych.

%prep
%setup -q -n %{name}-v%{ver}-%{vermin}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LIBDIR="%{_libdir}/ebtables" \
	BINDIR="%{_sbindir}" \
	MANDIR="%{_mandir}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/etc/sysconfig,/etc/rc.d/init.d,%{_sysconfdir}} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_libdir}/ebtables,%{_mandir}/man8}

install ebtables{,-restore}	$RPM_BUILD_ROOT%{_sbindir}
install ethertypes		$RPM_BUILD_ROOT%{_sysconfdir}
install ebtables.8		$RPM_BUILD_ROOT%{_mandir}/man8
install extensions/*.so	*.so	$RPM_BUILD_ROOT%{_libdir}/ebtables
install ebtables-save		$RPM_BUILD_ROOT%{_sbindir}
%{__sed} -i -e "s|__EXEC_PATH__|%{_sbindir}|g" $RPM_BUILD_ROOT%{_sbindir}/ebtables-save

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ebtables
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ebtables-config

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ebtables

%preun
if [ $1 -eq 0 ]; then
	%service ebtables stop
	/sbin/chkconfig --del ebtables
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog INSTALL THANKS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ethertypes
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ebtables-config
%attr(754,root,root) /etc/rc.d/init.d/ebtables
%attr(755,root,root) %{_sbindir}/ebtables*
%dir %{_libdir}/ebtables
%attr(755,root,root) %{_libdir}/ebtables/libebt*.so
%{_mandir}/man8/ebtables.8*
