Summary:	An implementation of LucasArts's SCUMM interpreter
Name:		scummvm
Version:	1.4.1
Release:	%mkrel 2
Source0:	http://prdownloads.sourceforge.net/scummvm/%{name}-%{version}.tar.bz2
Patch0:		scummvm-1.2.0-dont-strip.patch
License:	GPLv2+ and LGPLv2+
Url:		http://scummvm.sourceforge.net/
Group:		Games/Adventure
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(libmpeg2)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(fluidsynth)
BuildRequires:	nasm

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

%prep
%setup -q
%apply_patches

%build
%global optflags %{optflags} -O3 -ffast-math
%setup_compile_flags
./configure	--prefix=%{_prefix} \
		--bindir=%{_gamesbindir} \
		--mandir=%{_mandir} \
		--datadir=%{_gamesdatadir} \
		--enable-release \
		--enable-verbose-build \
		--enable-opengl \
		--enable-all-engines
%make NASMFLAGS="-Ox -gdwarf2 -f elf -Fdwarf"

%install
%__rm -rf %{buildroot}
%makeinstall_std

%__install -m644 dists/%{name}.desktop -D %{buildroot}%{_datadir}/applications/%{name}.desktop

%__install -m644 dists/maemo/scummvm48.png -D %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%__install -m644 dists/maemo/scummvm64.png -D %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%__install -m644 dists/motomagx/pep/scummvm_big_usr.png -D %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%__install -m644 icons/scummvm.svg -D %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%__mkdir_p %{buildroot}%{_datadir}/%{name}

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %{_docdir}/%{name}
%{_gamesbindir}/*
%{_mandir}/*/*
%{_datadir}/pixmaps/%{name}.xpm
%{_gamesdatadir}/*
%{_datadir}/applications/%{name}.desktop
%dir %{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}.*


%changelog
* Fri Feb 03 2012 Andrey Bondrov <abondrov@mandriva.org> 1.4.1-2mdv2012.0
+ Revision: 770988
- Update description and revert some recent changes for better rpm4 compatibility

* Wed Feb 01 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.4.1-1
+ Revision: 770533
- enable all engines
- fix so that nasm uses dwarf debug format as debugedit doesn't support stab
- enable opengl
- enable release mode
- link with %%ldflags
- make build verbose
- cleanup spec
- use pkgconfig() deps

  + Götz Waschk <waschk@mandriva.org>
    - update package description to mention drascula
    - new version

* Mon Nov 21 2011 Andrey Bondrov <abondrov@mandriva.org> 1.4.0-2
+ Revision: 732094
- Spec cleanup and description update

* Wed Nov 16 2011 Götz Waschk <waschk@mandriva.org> 1.4.0-1
+ Revision: 731120
- new version

* Thu Jul 28 2011 Götz Waschk <waschk@mandriva.org> 1.3.1-1
+ Revision: 692056
- import scummvm

