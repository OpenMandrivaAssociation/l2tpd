%define	name	l2tpd
%define	version	0.69
%define	release	%mkrel 15

Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Url:		http://www.l2tpd.org/
Group:		System/Servers
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}-init.bz2
# Minimal sample configuration file for use with FreeS/WAN
Source2:	%{name}.conf.bz2
Source3:        %{name}-options.l2tpd.bz2
# Two sample FreeS/WAN configuration files
Source4:        %{name}-L2TPD-PSK.conf.bz2
Source5:        %{name}-L2TPD-CERT.conf.bz2
#SysV style pty allocation patch from Debian(modified)
Patch0:		%{name}-pty.patch.bz2
#Close stdin for daemon mode
Patch1:		%{name}-close.patch.bz2
Patch2:		%{name}-cfgpath.patch.bz2
Patch3:		%{name}-0.69-gcc-3.3.patch.bz2
Patch4:		%{name}-0.69-gcc-3.4.patch.bz2
Patch5:         %{name}-0.69-gcc4.patch
BuildRoot:	%_tmppath/%{name}-%{version}-%{release}-buildroot
Summary:        User-space implementation of L2TP (RFC 2661) for Linux
Requires:	/sbin/chkconfig fileutils ppp
Requires(preun):rpm-helper

%description

l2tpd is an implementation of the layer two tunneling protocol. It works
in userspace completely (although kernel work is planned after the
userspace version is stablized).  l2tpd works by opening a pseudo-tty
for communicating with pppd.  Although l2tpd was written for Linux, the
current version should be highly portable to other UNIX's supported by
pppd.

A great place to get started:
http://www.jacco2.dds.nl/networking/freeswan-l2tp.html

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p1 -b .gcc34
%patch5 -p1 -b .gcc4

%build
%make DFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
#There's no 'install' rule in Makefile, let's do it manually
install -d $RPM_BUILD_ROOT%{_sbindir}
install -m755 %{name} $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT%{_mandir}/{man5,man8}
install -m644 doc/%{name}.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5
install -m644 doc/l2tp-secrets.5 $RPM_BUILD_ROOT%{_mandir}/man5
install -m644 doc/%{name}.8 $RPM_BUILD_ROOT%{_mandir}/man8
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{%{name},ppp,ipsec.d}
bzcat %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.conf
install -m644 %{SOURCE3} ${RPM_BUILD_ROOT}%{_sysconfdir}/ppp/options.l2tpd
install -m644 %{SOURCE4} ${RPM_BUILD_ROOT}%{_sysconfdir}/ipsec.d/L2TPD-PSK.conf
install -m644 %{SOURCE5} ${RPM_BUILD_ROOT}%{_sysconfdir}/ipsec.d/L2TPD-CERT.conf
install -m600 doc/l2tp-secrets.sample $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/l2tp-secrets
install -d $RPM_BUILD_ROOT%{_initrddir}
bzcat %{SOURCE1} > $RPM_BUILD_ROOT%{_initrddir}/%{name}; chmod 755 $RPM_BUILD_ROOT%{_initrddir}/%{name}

%post
# Uncomment the %_post_service line if you want to start l2tpd at boot.
# For security reasons it is commented out. The sysadmin should explicitly
# add it to the boot sequence (chkconfig --add l2tpd ; service l2tpd start)
# %_post_service %{name}

%preun
%_preun_service %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc BUGS CHANGELOG CREDITS LICENSE README TODO doc/{rfc2661.txt,%{name}.conf.sample}
%{_sbindir}/%{name}
%{_mandir}/*/*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/ppp/*
%dir %{_sysconfdir}/ipsec.d
%config(noreplace) %{_sysconfdir}/ipsec.d/*
%config(noreplace) %{_initrddir}/%{name}

