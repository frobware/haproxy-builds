Name:           Bear
Version:        2.4.4
Release:        1%{?dist}
Summary:        a tool to generate compilation database for Clang tooling

License:        GPLv3
URL:            https://github.com/rizsotto/Bear
Source0:        https://github.com/rizsotto/Bear/archive/refs/tags/${version}.tar.gz

%global debug_package %{nil}

%description
Bear - a tool to generate compilation database for Clang tooling.

%prep
%setup -q

%build
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix}
%{__make}

%install
%{__make} DESTDIR=%{buildroot} install

%files
%{_bindir}/bear
%{_libdir}/bear/libear.so
%{_docdir}/bear/COPYING
%{_docdir}/bear/ChangeLog.md
%{_docdir}/bear/README.md
%{_mandir}/man1/bear.1.gz
%{_datadir}/bash-completion
