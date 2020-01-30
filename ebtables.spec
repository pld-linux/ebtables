Summary:	Ethernet Bridge Tables
Summary(pl.UTF-8):	Ethernet Bridge Tables - filtrowanie i translacja adresów dla Ethernetu
Name:		ebtables
Version:	2.0.11
Release:	1
License:	GPL v2+
Group:		Networking/Daemons
Source0:	http://ftp.netfilter.org/pub/ebtables/%{name}-%{version}.tar.gz
# Source0-md5:	071c8b0a59241667a0044fb040d4fc72
Source1:	%{name}.init
Source2:	%{name}-config
URL:		http://ebtables.sourceforge.net/
# <linux/netfilter/xt_AUDIT.h>
BuildRequires:	linux-libc-headers >= 6:3.0
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Obsoletes:	iptables-ebtables
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
%setup -q

%build
%configure

%{__make}

%if 0
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LIBDIR="%{_libdir}/ebtables" \
	BINDIR="%{_sbindir}" \
	MANDIR="%{_mandir}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/sysconfig,/etc/rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# could be useful only for plugins development, but headers are not installed
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libebtc.{la,so}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ebtables
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ebtables-config

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
%attr(755,root,root) %{_sbindir}/ebtables-legacy
%attr(755,root,root) %{_sbindir}/ebtables-legacy-restore
%attr(755,root,root) %{_sbindir}/ebtables-legacy-save
%attr(755,root,root) %{_sbindir}/ebtablesd
%attr(755,root,root) %{_sbindir}/ebtablesu
%attr(755,root,root) %{_libdir}/libebtc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libebtc.so.0
%{_mandir}/man8/ebtables-legacy.8*
