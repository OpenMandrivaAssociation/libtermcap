%define	major	2
%define	libname	%mklibname termcap %{major}
%define	devname	%mklibname termcap -d

Summary:	A basic system library for accessing the termcap database
Name:		libtermcap
Version:	2.0.8
Release:	55
Source0:	termcap-%{version}.tar.bz2
Url:		ftp://metalab.unc.edu/pub/Linux/GCC/
License:	LGPL+
Group:		System/Libraries
Patch0:		termcap-2.0.8-shared.patch
Patch1:		termcap-2.0.8-setuid.patch
Patch2:		termcap-2.0.8-instnoroot.patch
Patch3:		termcap-2.0.8-compat21.patch
Patch4:		termcap-2.0.8-xref.patch
Patch5:		termcap-2.0.8-fix-tc.patch
Patch6:		termcap-2.0.8-ignore-p.patch
Patch7:		termcap-buffer.patch
# This patch is a REALLY BAD IDEA without patch #10 below....
Patch8:		termcap-2.0.8-bufsize.patch
Patch9:		termcap-2.0.8-colon.patch
Patch10:	libtermcap-aaargh.patch
# (gc) conflicting definition of `bcopy' against latest glibc 2.1.95
Patch11:	termcap-fix-glibc-2.2.patch
Patch12:	termcap-2.0.8-LDFLAGS.diff
Patch13:	termcap-2.0.8-add-info-dir-metadata-to-info-page.patch
BuildRequires:	texinfo

%description
The libtermcap package contains a basic system library needed to access
the termcap database.  The termcap library supports easy access to the
termcap database, so that programs can output character-based displays in
a terminal-independent manner.

%package -n	%{libname}
Summary:	Development tools for programs which will access the termcap database
Group:		System/Libraries
Requires:	termcap

%description -n	%{libname}
The libtermcap package contains a basic system library needed to access
the termcap database.  The termcap library supports easy access to the
termcap database, so that programs can output character-based displays in
a terminal-independent manner.

%package -n	%{devname}
Summary:	Development tools for programs which will access the termcap database
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	termcap-devel = %{version}-%{release}

%description -n	%{devname}
This package includes the libraries and header files necessary for
developing programs which will access the termcap database.

If you need to develop programs which will access the termcap database,
you'll need to install this package.  You'll also need to install the
libtermcap package.

%prep
%setup -q -n termcap-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .nochown
%patch3 -p1 -b .compat21
%patch4 -p1
%patch5 -p1 -b .fix-tc
%patch6 -p1 -b .ignore-p
%patch7 -p1 -b .buffer
%patch8 -p1 -b .bufsize
%patch9 -p1 -b .colon
%patch10 -p1 -b .aaargh
%patch11 -p0
%patch12 -p0
%patch13 -p1 -b .infometa~

%build
%make CFLAGS="%{optflags} -I." LDFLAGS="%{ldflags}"

%install
rm -rf %{buildroot}
# (gb) They should do proper Makefiles

mkdir -p %{buildroot}/%{_lib}
install -m 755 libtermcap.so.%{major}.* %{buildroot}/%{_lib}/
ln -sr %{buildroot}/%{_lib}/libtermcap.so.%{major}.* %{buildroot}/%{_lib}/libtermcap.so.2

install -m644 libtermcap.a -D %{buildroot}%{_libdir}/libtermcap.a
ln -sr %{buildroot}/%{_lib}/libtermcap.so.%{major}.* %{buildroot}%{_libdir}/libtermcap.so

mkdir -p %{buildroot}%{_infodir}
install -m644 termcap.info* %{buildroot}%{_infodir}/

mkdir -p %{buildroot}%{_includedir}
install -m644 termcap.h -D %{buildroot}%{_includedir}/termcap.h

# cleanup
rm -f %{buildroot}%{_libdir}/libtermcap.a

%files -n %{libname}
/%{_lib}/libtermcap.so.%{major}*

%files -n %{devname}
%doc ChangeLog README
%{_infodir}/termcap.info*
%{_libdir}/libtermcap.so
%{_includedir}/termcap.h

%changelog
* Sat Jan  6 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.0.8-55
- only create libtermcap.so symlink in %{_libdir}
- add info dir section & entry metadata to termcap.info (P13) so that it can be
  automatically handlded by file triggers rather than explicit pkg scriptlet
- add dependency on 'termcap' for termcap package as it's no longer
  required by 'basesystem-minimal'
- cosmetics

* Wed Dec 21 2011 Matthew Dawkins <mattydaw@mandriva.org> 2.0.8-53
+ Revision: 744177
- try to pipe info output if installed with excludedocs
- and to keep from failing to uninstalling

* Thu Dec 15 2011 Oden Eriksson <oeriksson@mandriva.com> 2.0.8-52
+ Revision: 741594
- various cleanups

* Fri Apr 29 2011 Oden Eriksson <oeriksson@mandriva.com> 2.0.8-51
+ Revision: 660285
- mass rebuild

* Thu Nov 25 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.8-50mdv2011.0
+ Revision: 601061
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.8-49mdv2010.1
+ Revision: 519827
- rebuild

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.0.8-48mdv2010.0
+ Revision: 425754
- rebuild

* Thu Dec 25 2008 Oden Eriksson <oeriksson@mandriva.com> 2.0.8-47mdv2009.1
+ Revision: 319034
- use %%ldflags (P12)

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 2.0.8-46mdv2009.0
+ Revision: 223009
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 2.0.8-45mdv2008.1
+ Revision: 178950
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag
    - rebuild

* Fri Aug 10 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.0.8-43mdv2008.0
+ Revision: 61056
- update scriptlet for info page to use lzma suffix
- wipe out buildroot in %%install, not %%prep
- drop BuildRoot & %%clean
- cosmetics

* Mon Aug 06 2007 Götz Waschk <waschk@mandriva.org> 2.0.8-42mdv2008.0
+ Revision: 59225
- fix wrong obsoletes in libtermcap-devel

* Sat Aug 04 2007 Adam Williamson <awilliamson@mandriva.org> 2.0.8-41mdv2008.0
+ Revision: 58795
- rebuild for 2008
- move docs to -devel package
- new devel policy
- bunzip2 patches



* Mon Jul 31 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.0.8-40mdv2007.0
- fix installation in "urpmi --root" case
- fix some rpmlint warnings

* Wed May 17 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.0.8-39mdk
- more prereq fixes (for the "urpmi --root" case)

* Tue May 16 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.0.8-38mdk
- fix prereq

* Tue Dec 20 2005 Lenny Cartier <lenny@mandriva.com> 2.0.8-37mdk
- rebuild

* Fri Sep 10 2004 Lenny Cartier <lenny@mandrakesoft.com> 2.0.8-36mdk
- rebuild

* Mon Aug  4 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.8-35mdk
- Put back libtermcap-devel provides as nobody uses termcap-devel

* Thu Jul 10 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.8-34mdk
- Fix libification, mklibname'ize

* Thu Jan 26 2003 Lenny Cartier <lenny@mandrakesoft.com> 2.0.8-33mdk
- rebuild

* Tue Jun 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.8-32mdk
- rpmlint fixes: hardcoded-library-path

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.8-31mdk
- Automated rebuild in gcc3.1 environment

* Mon Jul 30 2001 Lenny Cartier <lenny@mandrakesoft.com> 2.0.8-30mdk
- rebuild

* Sun May 27 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.0.8-29mdk
- build with RPM_OPT_FLAGS

* Mon Mar 26 2001 Pixel <pixel@mandrakesoft.com> 2.0.8-28mdk
- eurk, comments are given to ldconfig in %%post :-(

* Mon Mar 26 2001 Pixel <pixel@mandrakesoft.com> 2.0.8-27mdk
- fixed yet again stupid PreReq on bash (post and postun invocation).

* Fri Mar 23 2001 David BAUDENS <baudens@mandrakesoft.com> 2.0.8-26mdk
- Fix Provides and Obsoletes

* Tue Mar 20 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.8-25mdk
- fix provides and obsoletes

* Mon Mar 19 2001 Lenny Cartier <lenny@mandrakesoft.com> 2.0.8-24mdk
- obsoletes libtermcap

* Sat Mar 17 2001 Lenny Cartier <lenny@mandrakesoft.com> 2.0.8-23mdk
- split

* Fri Jan 12 2001 Fran?ois Pons <fpons@mandrakesoft.com> 2.0.8-22mdk
- fixed stupid PreReq on bash (post and postun invocation).

* Fri Jan 12 2001 David BAUDENS <baudens@mandrakesoft.com> 2.0.8-21mdk
- BuildRequires: texinfo
- Spec clean up

* Fri Oct 27 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.8-20mdk
- fix compile with latest glibc

* Thu Aug 31 2000 Etienne Faure <etienne@mandrakesoft.com> 2.0.8-19mdk
- rebuild with %%doc and _infodir macros

* Tue Mar 23 2000 Lenny Cartier <lenny@mandrakesoft.com> 2.0.8-18mdk
- fix group

* Sat Mar  4 2000 Pixel <pixel@mandrakesoft.com> 2.0.8-17mdk
- moved the info to libtermcap-devel
(that way libtermcap doesn't require bash which require libtermcap ;-)
- %%trigger transformed in %%post

* Mon Dec 20 1999 Jerome Martin <jerome@mandrakesoft.com>
- Rebuild for ne environment

* Wed Nov  3 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- RH merges.
- ignore the first argument to tgetent, so the last change doesn't
  keep blowing up programs.(r)
- ignore the second argument to tgetstr() as well.(r)
- increase default size of malloc'ed tgetent buffer from 1024 to 1536.(r)
- don't shrink colons (r).
- add buffer overflow patch from Kevin Vajk <kvajk@ricochet.net>(r)
- permit multiple tc= continuations and ignore unnecessary %%p ("push arg") (r)
- fix to make the texi documenattion compile(r)
- use __PMT(...) prototypes (r)

* Wed Apr 14 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add files /lib/libtermcap.so.2

* Mon Apr 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- add patch to for the termcap.texi with a wrong reference.
- Remove typo with bzip2.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Thu Jan 14 1999 Jeff Johnson <jbj@redhat.com>
- use __PMT(...) prototypes (#761)

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Wed Aug 05 1998 Erik Troan <ewt@redhat.com>
- run install-info from a %%trigger so we don't have to make it a prereq; as
  termcap is used by bash, the install ordering issues are hairy
- commented out the chown stuff from 'make install' so you don't have to
  be root to build this
- don't run ldconfig if prefix= is used during 'make install'

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- build root.

* Tue Jun 30 1998 Alan Cox <alan@redhat.com>
- But assume system termcap is sane. Also handle setfsuid return right.

* Tue Jun 30 1998 Alan Cox <alan@redhat.com>
- TERMCAP environment hole for setuid apps squished.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Oct 14 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups

* Tue Jun 03 1997 Erik Troan <ewt@redhat.com>
- built against glibc
