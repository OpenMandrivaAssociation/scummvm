# As of 2.1.0 LTO should be disabled or build error apperars: Checking endianness... unknown
# fixing it by sed or patch (applied previous to ver 1.8.0) or new wont work due to segmentation fault
#dwp -e scummvm
#make: *** [Makefile.common:94: scummvm.dwp] Segmentation fault (core dumped)
# Solution = build without patch and LTO. Alternatively you can try with GCC (angry)
# Workaround suggested by crazy - apply drop-split-dwarf-want-lto and reenable LTO. LTO enable by sed.

%define _disable_lto 1

Summary:	An implementation of LucasArts's SCUMM interpreter
Name:		scummvm
Version:	2.5.0
Release:	1
License:	GPLv2+ and LGPLv2.1+
Group:		Games/Adventure
Url:		http://scummvm.org/
Source0:	http://scummvm.org/frs/%{name}/%{version}/%{name}-%{version}.tar.xz
#Patch0:		drop-split-dwarf-want-lto.patch

BuildRequires:	nasm
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(fluidsynth)
BuildRequires:	pkgconfig(libmpeg2)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(vorbis)

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
%setup -q
%autopatch -p1

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
		--enable-c++11 \
		--enable-all-engines
%make_build NASMFLAGS="-Ox -gdwarf2 -f elf -Fdwarf" STRIP="true"

%install
%make_install STRIP="true"

install -m644 dists/%{name}.desktop -D %{buildroot}%{_datadir}/applications/%{name}.desktop

install -m644 dists/maemo/scummvm48.png -D %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
install -m644 dists/maemo/scummvm64.png -D %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
#install -m644 dists/motomagx/pep/scummvm_big_usr.png -D %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -m644 icons/scummvm.svg -D %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

mkdir -p %{buildroot}%{_datadir}/%{name}

%files
%doc %{_docdir}/%{name}
%{_gamesbindir}/*
%{_mandir}/*/*
%{_datadir}/pixmaps/%{name}.xpm
%{_gamesdatadir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/metainfo/scummvm.appdata.xml
%dir %{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}.*
