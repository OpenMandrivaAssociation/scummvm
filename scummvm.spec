#define snapshot 20230616
# Plugins reference symbols from scummvm
%define _disable_ld_no_undefined 1

Summary:	An implementation of LucasArts's SCUMM interpreter
Name:		scummvm
Version:	2.9.0
Release:	%{?snapshot:0.%{snapshot}.}1
License:	GPLv2+ and LGPLv2.1+
Group:		Games/Adventure
Url:		https://scummvm.org/
Source0:	%{?snapshot:https://github.com/scummvm/scummvm/archive/refs/heads/master.tar.gz#/%{name}-%{snapshot}.tar.gz}%{!?snapshot:http://scummvm.org/frs/%{name}/%{version}/%{name}-%{version}.tar.gz}
#Patch0:		drop-split-dwarf-want-lto.patch

BuildRequires:	nasm
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(fluidsynth)
BuildRequires:	pkgconfig(libmpeg2)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(SDL2_net)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	giflib-devel
BuildRequires:	pkgconfig(vpx)
BuildRequires:	pkgconfig(liba52)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libmikmod)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(lua)
# Optional, but sadly main can't depend on restricted
#BuildRequires:	pkgconfig(faad2)

%description
ScummVM is an implementation of LucasArts S.C.U.M.M.
(Script Creation Utility for Maniac Mansion) interpreter, used in games
such as Monkey Island, Indiana Jones, Day Of The Tentacle, Sam and Max,
and many more. Some things are still missing, and some games cannot
be completeted yet. There are quite a few known bugs. Regardless of
the bugs it is still possible to play many games all the way through
to the end. Still other games do not load at all.

Some games such as "Beneath A Steel Sky", "Flight Of The Amazon Queen"
and "Drascula: The Vampire Strikes Back" have been released by their
developers. Install beneath-a-steel-sky, flight-of-the-amazon-queen and
drascula packages from non-free repository to play.

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{?snapshot:master}%{!?snapshot:%{version}}

%build
#export CC=gcc
#export CXX=g++
# Sed to fix endianness check fail caused by LTO enabled.
sed -i '/tmp_endianness_check.cpp/ s/$CXXFLAGS/$CXXFLAGS -fno-lto -O0/' configure
%setup_compile_flags

#ifarch %{ix86}
# gold fails on i586
#export CXX="%{__cxx} -fuse-ld=bfd"
#endif

./configure	--prefix=%{_prefix} \
		--bindir=%{_gamesbindir} \
		--mandir=%{_mandir} \
		--datadir=%{_gamesdatadir} \
		--enable-release \
		--enable-verbose-build \
		--enable-plugins \
		--default-dynamic \
		--enable-optimizations \
		--opengl-mode=any \
		--enable-all-engines
%make_build NASMFLAGS="-Ox -gdwarf2 -f elf -Fdwarf" STRIP="true"

%install
%make_install STRIP="true"

mkdir -p %{buildroot}%{_datadir}/%{name}

%files
%doc %{_docdir}/%{name}
%{_gamesbindir}/*
%{_mandir}/*/*
%{_gamesdatadir}/*
%{_datadir}/applications/org.scummvm.scummvm.desktop
%{_datadir}/metainfo/org.scummvm.scummvm.metainfo.xml
%dir %{_datadir}/%{name}
%{_datadir}/icons/hicolor/scalable/apps/org.scummvm.scummvm.svg
%{_datadir}/pixmaps/org.scummvm.scummvm.xpm
%dir %{_prefix}/lib/scummvm
# FIXME split the various engines into subpackages
%{_prefix}/lib/scummvm/*
