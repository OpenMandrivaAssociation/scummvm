%define	name	scummvm
%define version 1.3.1
%define rel 1
%define release %mkrel %rel
%define Summary	An implementation of LucasArts's SCUMM interpreter

Summary:	%{Summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://prdownloads.sourceforge.net/scummvm/%{name}-%{version}.tar.bz2
Patch0: scummvm-1.2.0-dont-strip.patch
License:	GPLv2+ and LGPLv2+
Url:		http://scummvm.sourceforge.net/
Group:		Games/Adventure
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	SDL-devel 
BuildRequires:	ncurses-devel
BuildRequires:	mad-devel 
BuildRequires:	oggvorbis-devel 
BuildRequires:	libmpeg2dec-devel
BuildRequires:	libflac-devel
BuildRequires:	libfluidsynth-devel
BuildRequires:	nasm

%description
ScummVM is an implementation of LucasArts S.C.U.M.M.
(Script Creation Utility for Maniac Mansion) interpreter, used in games
such as Monkey Island, Indiana Jones, Day Of The Tentacle, Sam and Max,
and many more. Some things are still missing, and some games cannot
be completeted yet. There are quite a few known bugs. Regardless of
the bugs it is still possible to play some games all the way through 
to the end. Still other games do not load at all.

Some games such as "Beneath a steel sky" have been released by their
developers, install scummvm-beneath-a-steel-sky packages to play

%prep
%setup -q
%apply_patches

%build
#gw format string errors in 1.0.0
%define Werror_cflags %nil
./configure --prefix=%_prefix --bindir=%_gamesbindir --mandir=%_mandir \
  --datadir=%_gamesdatadir

#Don't want *alot* of warnings about multiline comments...
%make CXXFLAGS="$RPM_OPT_FLAGS -O3 -ffast-math -Wuninitialized -Wno-long-long -Wno-multichar -Wno-unknown-pragmas"

%install
rm -rf $RPM_BUILD_ROOT installed-docs
%makeinstall_std 
mv %buildroot%_datadir/doc/%name installed-docs

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cp dists/%name.desktop $RPM_BUILD_ROOT%{_datadir}/applications

install -D -m 644 dists/maemo/scummvm48.png %buildroot%_datadir/icons/hicolor/48x48/apps/%name.png
install -D -m 644 dists/maemo/scummvm64.png %buildroot%_datadir/icons/hicolor/64x64/apps/%name.png
install -D -m 644 dists/motomagx/pep/scummvm_big_usr.png %buildroot%_datadir/icons/hicolor/32x32/apps/%name.png
install -D -m 644 icons/scummvm.svg %buildroot%_datadir/icons/hicolor/scalable/apps/%name.svg


mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc installed-docs/*
%{_gamesbindir}/*
%{_mandir}/*/*
%{_datadir}/pixmaps/%{name}.xpm
%_gamesdatadir/*
%_datadir/applications/%name.desktop
%dir %{_datadir}/%{name}
%_datadir/icons/hicolor/*/apps/%name.*

