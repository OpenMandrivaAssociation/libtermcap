%define name	libtermcap
%define version	2.0.8
%define release	%mkrel 41

%define major		2
%define libname_orig	libtermcap
%define libname		%mklibname termcap %{major}
%define develname	%mklibname termcap -d

Summary:	A basic system library for accessing the termcap database
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source:		termcap-%{version}.tar.bz2
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

%package -n %{libname}
Summary:        Development tools for programs which will access the termcap database
Group:          System/Libraries
Obsoletes:	%{libname_orig}
Provides:	%{libname_orig}

%description -n %{libname}
The libtermcap package contains a basic system library needed to access
the termcap database.  The termcap library supports easy access to the
termcap database, so that programs can output character-based displays in
a terminal-independent manner.

%package -n %{develname}
Summary:	Development tools for programs which will access the termcap database
Group:		Development/C
Requires:	%{libname} = %version
Obsoletes:	%{libname_orig}-devel
Provides:	%{libname_orig}-devel = %{version}-%{release}
Provides:	termcap-devel = %{version}-%{release}
Obsoletes:	%{mklibname termcap 2 -d}

%description -n %{develname}
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
%posttrans -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post -n %{develname}
/sbin/install-info \
	--section="Libraries" --entry="* Termcap: (termcap).               The GNU termcap library." \
	--info-dir=%{_infodir} %{_infodir}/termcap.info.bz2

%postun -n %{develname}
if [ $1 = 0 ]; then
    /sbin/install-info --delete \
	--section="Libraries" --entry="* Termcap: (termcap).               The GNU termcap library." \
	--info-dir=%{_infodir} %{_infodir}/termcap.info.bz2
fi

%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc ChangeLog README
/%{_lib}/*.so
%{_infodir}/termcap.info*
%_libdir/libtermcap.a
%_libdir/libtermcap.so
%_includedir/termcap.h
