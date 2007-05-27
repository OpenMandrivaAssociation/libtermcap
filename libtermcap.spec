%define name	libtermcap
%define version	2.0.8
%define release	%mkrel 40

%define lib_major	2
%define lib_name_orig	libtermcap
%define lib_name	%mklibname termcap %{lib_major}

Summary:	A basic system library for accessing the termcap database
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source:		termcap-%{version}.tar.bz2
Url:		ftp://metalab.unc.edu/pub/Linux/GCC/
License:	LGPL
Group:		System/Libraries

Patch0:		termcap-2.0.8-shared.patch.bz2
Patch1:		termcap-2.0.8-setuid.patch.bz2
Patch2:		termcap-2.0.8-instnoroot.patch.bz2
Patch3:		termcap-2.0.8-compat21.patch.bz2
Patch4:		termcap-2.0.8-xref.patch.bz2
Patch5:		termcap-2.0.8-fix-tc.patch.bz2
Patch6:		termcap-2.0.8-ignore-p.patch.bz2
Patch7:		termcap-buffer.patch.bz2
# This patch is a REALLY BAD IDEA without patch #10 below....
Patch8:		termcap-2.0.8-bufsize.patch.bz2
Patch9:		termcap-2.0.8-colon.patch.bz2
Patch10:	libtermcap-aaargh.patch.bz2
# (gc) conflicting definition of `bcopy' against latest glibc 2.1.95
Patch11:	termcap-fix-glibc-2.2.patch.bz2

Requires:	%_sysconfdir/termcap
Requires(posttrans):	ldconfig glibc
Requires(postun):	ldconfig
BuildRoot:	%_tmppath/%name-%version-%release-root
BuildRequires:	texinfo

%description
The libtermcap package contains a basic system library needed to access
the termcap database.  The termcap library supports easy access to the
termcap database, so that programs can output character-based displays in
a terminal-independent manner.

%package -n %{lib_name}
Summary:        Development tools for programs which will access the termcap database
Group:          System/Libraries
Obsoletes:	%{lib_name_orig}
Provides:	%{lib_name_orig}

%description -n %{lib_name}
The libtermcap package contains a basic system library needed to access
the termcap database.  The termcap library supports easy access to the
termcap database, so that programs can output character-based displays in
a terminal-independent manner.

%package -n %{lib_name}-devel
Summary:	Development tools for programs which will access the termcap database
Group:		Development/C
Requires:	%{lib_name} = %version
Obsoletes:	%{lib_name_orig}-devel
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	termcap-devel = %{version}-%{release}

%description -n %{lib_name}-devel
This package includes the libraries and header files necessary for
developing programs which will access the termcap database.

If you need to develop programs which will access the termcap database,
you'll need to install this package.  You'll also need to install the
libtermcap package.

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q -n termcap-2.0.8
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

%build
%make CFLAGS="$RPM_OPT_FLAGS -I."

%install
# (gb) They should do proper Makefiles

mkdir -p $RPM_BUILD_ROOT/%{_lib}
install -m 755 libtermcap.so.* $RPM_BUILD_ROOT/%{_lib}/
ln -s libtermcap.so.2.0.8 $RPM_BUILD_ROOT/%{_lib}/libtermcap.so
ln -s libtermcap.so.2.0.8 $RPM_BUILD_ROOT/%{_lib}/libtermcap.so.2

mkdir -p $RPM_BUILD_ROOT%{_libdir}
install -m 644 libtermcap.a $RPM_BUILD_ROOT%{_libdir}/
ln -s ../../%{_lib}/libtermcap.so.2.0.8 $RPM_BUILD_ROOT%{_libdir}/libtermcap.so

mkdir -p $RPM_BUILD_ROOT%{_infodir}
install -m 644 termcap.info* $RPM_BUILD_ROOT%{_infodir}/

mkdir -p $RPM_BUILD_ROOT%{_includedir}
install -m 644 termcap.h $RPM_BUILD_ROOT%{_includedir}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -m 644 termcap.src $RPM_BUILD_ROOT%{_sysconfdir}/termcap

rm -f $RPM_BUILD_ROOT%_sysconfdir/termcap

%clean
rm -fr %buildroot

# pixel: KEEP LDCONFIG WITH "-p" OR COME TALK TO ME 
%posttrans -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%post -n %{lib_name}-devel
/sbin/install-info \
	--section="Libraries" --entry="* Termcap: (termcap).               The GNU termcap library." \
	--info-dir=%{_infodir} %{_infodir}/termcap.info.bz2

%postun -n %{lib_name}-devel
if [ $1 = 0 ]; then
    /sbin/install-info --delete \
	--section="Libraries" --entry="* Termcap: (termcap).               The GNU termcap library." \
	--info-dir=%{_infodir} %{_infodir}/termcap.info.bz2
fi

%files -n %{lib_name}
%defattr(-,root,root)
%doc ChangeLog README
/%{_lib}/*.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
/%{_lib}/*.so
%{_infodir}/termcap.info*
%_libdir/libtermcap.a
%_libdir/libtermcap.so
%_includedir/termcap.h
