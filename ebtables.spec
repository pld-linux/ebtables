#
# TODO:
#	- initscripts stuff - move save/restore dumps to /etc/sysconfig & more
#	- review llh patch
#
%define		_rel	1
%define		_pre	2
Summary:	Ethernet Bridge Tables
Summary(pl.UTF-8):	Ethernet Bridge Tables - filtrowanie i translacja adresów dla Ethernetu
Name:		ebtables
Version:	2.0.8
Release:	0.%{_pre}.%{_rel}
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/ebtables/%{name}-v%{version}-%{_pre}.tar.gz
# Source0-md5:	66bcbcb2dcf3b981ad4e86e1720e796e
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
%setup -q -n %{name}-v%{version}-%{_pre}

%build
%{__make} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT/etc/sysconfig
install -d $RPM_BUILD_ROOT%{_mandir}/man8
install -d $RPM_BUILD_ROOT%{_libdir}/ebtables
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

install ebtables		$RPM_BUILD_ROOT%{_sbindir}
install ebtables-restore	$RPM_BUILD_ROOT%{_sbindir}
install ethertypes		$RPM_BUILD_ROOT%{_sysconfdir}
install ebtables.8		$RPM_BUILD_ROOT%{_mandir}/man8
install extensions/*.so		$RPM_BUILD_ROOT%{_libdir}/ebtables
install *.so         		$RPM_BUILD_ROOT%{_libdir}/ebtables

export __iets=`printf %{_sbindir} | sed 's/\\//\\\\\\//g'`
export __iets2=`printf %{_mysysconfdir} | sed 's/\\//\\\\\\//g'`
sed -i "s/__EXEC_PATH__/$__iets/g" ebtables-save
install ebtables-save 		$RPM_BUILD_ROOT%{_sbindir}
sed -i "s/__EXEC_PATH__/$__iets/g" ebtables.sysv; sed -i "s/__SYSCONFIG__/$__iets2/g" ebtables.sysv
install ebtables.sysv		$RPM_BUILD_ROOT/etc/rc.d/init.d/ebtables
sed -i "s/__SYSCONFIG__/$__iets2/g" ebtables-config
install ebtables-config		$RPM_BUILD_ROOT/etc/sysconfig

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
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/ebtables
%attr(755,root,root) %{_libdir}/ebtables/*.so
%{_mandir}/man8/ebtables.8*
