Summary:	Ethernet Bridge Tables
Summary(pl):	Ethernet Bridge Tables - filtrowanie i translacja adresów dla Ethernetu
Name:		ebtables
Version:	2.0.6
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/%{name}/%{name}-v%{version}.tar.gz
# Source0-md5:	c4559af2366c764c6c42a3fdd40d60d3
Patch0:		%{name}-llh.patch
URL:		http://ebtables.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The ebtables project is the Linux 2.5.x (and above) Link Layer
firewalling subsystem, a patch for 2.4.x is maintained too. It
delivers for Linux the functionality of Ethernet frame filtering, all
kinds of frame NAT (Network Address Translation) and frame matching.
The ebtables infrastructure is a part of the standard Linux 2.5.x (and
above) kernels.

%description -l pl
Projekt ebtables to podsystem firewallingu na poziomie ³±cza dla
Linuksa w wersjach 2.5.x i nowszych (dostêpna jest te¿ ³ata do 2.4.x).
Dostarcza dla Linuksa funkcjonalno¶æ filtrowania ramek ethernetowych,
wszystkie rodzaje translacji adresów (NAT) dla ramek oraz
dopasowywanie ramek. Infrastruktura ebtables jest czê¶ci±
standardowych j±der Linuksa w wersjach 2.5.x i nowszych.

%prep
%setup -q -n %{name}-v%{version}
%patch0 -p1

%build
%{__make} CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -D ebtables	$RPM_BUILD_ROOT%{_sbindir}/ebtables
install -D ebtables.8	$RPM_BUILD_ROOT%{_mandir}/man8/ebtables.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
