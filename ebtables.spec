Summary:	Ethernet Bridge Tables
Name:		ebtables
Version:	2.0.2
Release:	0.1
License:	GPL
Group:		Networking/Daemons
URL:		http://ebtables.sourceforge.net/
Source0:	http://ebtables.sourceforge.net/v2.0/v2.0./%{name}-v%{version}.tar.gz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The ebtables project is the Linux 2.5.x (and above) Link Layer
firewalling subsystem, a patch for 2.4.x is maintained too. It
delivers for Linux the functionality of Ethernet frame filtering, all
kinds of frame NAT (Network Address Translation) and frame matching.
The ebtables infrastructure is a part of the standard Linux 2.5.x (and
above) kernels.

%prep
%setup -q -n %{name}-v%{version}

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
