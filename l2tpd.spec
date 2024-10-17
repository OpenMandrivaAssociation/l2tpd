%define	name	l2tpd
%define	version	0.69
%define	release	%mkrel 21

Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL v2
Url:		https://l2tpd.sourceforge.net/
Group:		System/Servers
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}-init.bz2
# Minimal sample configuration file for use with FreeS/WAN
Source2:	%{name}.conf.bz2
Source3:        %{name}-options.l2tpd.bz2
# Two sample FreeS/WAN configuration files
Source4:        %{name}-L2TPD-PSK.conf
Source5:        %{name}-L2TPD-CERT.conf
#SysV style pty allocation patch from Debian(modified)
Patch0:		%{name}-pty.patch
#Close stdin for daemon mode
Patch1:		%{name}-close.patch
Patch2:		%{name}-cfgpath.patch
Patch3:		%{name}-0.69-gcc-3.3.patch
Patch4:		%{name}-0.69-gcc-3.4.patch
Patch5:         %{name}-0.69-gcc4.patch
BuildRoot:	%_tmppath/%{name}-%{version}-%{release}-buildroot
Summary:        User-space implementation of L2TP (RFC 2661) for Linux
Requires:	chkconfig coreutils ppp
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



%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0.69-21mdv2011.0
+ Revision: 620045
- the mass rebuild of 2010.0 packages

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 0.69-20mdv2010.0
+ Revision: 438173
- rebuild

* Tue Oct 14 2008 Michael Scherer <misc@mandriva.org> 0.69-19mdv2009.1
+ Revision: 293708
- bunzip patches
- fix license, and website
- bunzip the configuration, that was placed on disk directly compressed

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - fix spacing at top of description

* Fri Feb 08 2008 Thierry Vignaud <tv@mandriva.org> 0.69-16mdv2008.1
+ Revision: 164089
- require coreutils instead of fileutils
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Dec 04 2007 Thierry Vignaud <tv@mandriva.org> 0.69-15mdv2008.1
+ Revision: 114920
- kill file require on chkconfig
- import l2tpd


* Fri Oct 28 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.69-15mdk
- Fix previous changelog
	- Add patch 5 : fix gcc 4 build 
	- Fix PreReq

* Fri Oct 28 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.69-14mdk
- Rebuild

* Sun Jul 25 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.69-13mdk
- fix gcc 3.4 build (P4)

* Wed Jul 23 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.69-12mdk
- fix gcc-3.3 patch (P3)

* Sun Jul 13 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.69-11mdk
- drop debug flags
- fix gcc-3.3 build

* Sun Jul 13 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.69-10mdk
- rebuild

* Thu May 01 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.69-9mdk
- distlint error

* Wed Mar 05 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.69-8mdk
- Requires =~ s/pppd/ppp/

* Mon Feb 10 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.69-7mdk
- Cleanups
- Merged in some of Jacco de Leeuw <jacco2@dds.nl>'s stuff:
	- Added 'connect-delay' to PPP parameters. This should solve
	  the Windows 2000 Professional "loopback detected" error.
	- Config path changed from /etc/l2tp to /etc/l2tpd (seems more logical).
	- Do not run at boot or install. The original RPM uses a config file
	  which is completely commented out, but it still starts l2tpd on all
	  interfaces. Could be a security risk. This RPM does not start l2tpd,
	  the sysadmin has to edit the config file and start l2tpd explicitly.
	- Renamed patches to start with l2tpd-
	- Added some of Jacco's config files
	      

* Sat Feb 01 2003 Lenny Cartier <lenny@mandrakesoft.com 0.69-6mdk
- rebuild

* Sat Nov 23 2002 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.69-5mdk
- bzip2'ed Source1
- Fixed init script
- config(noreplace) in files

* Sat Nov 23 2002 Per Øyvind Karlsen <peroyvind@delonic.no> 0.69-4mdk
- Changed permission on secrets file(thanks to Jacco de Leeuw)
- Added pppd to Requires(thannks to Jacco again;)
- Minor cleanups
- Added a more safe default config with acl enabled

* Mon Oct 21 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.69-3mdk
- from Per Øyvind Karlsen <peroyvind@delonic.no> :
	- PreReq and Requires
	- Fix preun_service

* Thu Oct 17 2002 Per Øyvind Karlsen <peroyvind@delonic.no> 0.69-2mdk
- Move l2tpd from /usr/bin to /usr/sbin
- Added SysV initscript
- Patch0
- Patch1

* Thu Oct 17 2002 Per Øyvind Karlsen <peroyvind@delonic.no> 0.69-1mdk
- Initial release
