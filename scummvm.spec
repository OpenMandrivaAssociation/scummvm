%define _disable_lto 1

Summary:	An implementation of LucasArts's SCUMM interpreter
Name:		scummvm
Version:	2.1.0
Release:	1
License:	GPLv2+ and LGPLv2.1+
Group:		Games/Adventure
Url:		http://scummvm.org/
Source0:	http://scummvm.org/frs/%{name}/%{version}/%{name}-%{version}.tar.xz
Patch0:		scummvm-2.1-fix-openmandriva.patch
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
%autopatch -p0

%build
%setup_compile_flags

%ifarch %{ix86}
# gold fails on i586
export CXX="%{__cxx} -fuse-ld=bfd"
%endif

./configure	--prefix=%{_prefix} \
		--bindir=%{_gamesbindir} \
		--mandir=%{_mandir} \
		--datadir=%{_gamesdatadir} \
		--enable-release \
		--enable-verbose-build \
		--enable-c++11 \
		--enable-all-engines
%make NASMFLAGS="-Ox -gdwarf2 -f elf -Fdwarf" STRIP="true"

%install
%makeinstall_std STRIP="true"

install -m644 dists/%{name}.desktop -D %{buildroot}%{_datadir}/applications/%{name}.desktop

install -m644 dists/maemo/scummvm48.png -D %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
install -m644 dists/maemo/scummvm64.png -D %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
install -m644 dists/motomagx/pep/scummvm_big_usr.png -D %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -m644 icons/scummvm.svg -D %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

mkdir -p %{buildroot}%{_datadir}/%{name}

%files
%doc %{_docdir}/%{name}
%{_gamesbindir}/*
%{_mandir}/*/*
%{_datadir}/pixmaps/%{name}.xpm
%{_gamesdatadir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%dir %{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}.*
