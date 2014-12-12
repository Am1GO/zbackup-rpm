%global _hardened_build 1

Name:		zbackup
Version:	1.3
Release:	3%{?dist}
Summary:	A versatile deduplicating backup tool

License:	GPLv2+ and OpenSSL
URL:		http://zbackup.org/
Source0:	https://github.com/zbackup/zbackup/archive/%{version}.tar.gz

BuildRequires:	cmake >= 2.8.2
BuildRequires:	xz-devel
BuildRequires:	openssl-devel
BuildRequires:	protobuf-devel
BuildRequires:	zlib-devel
BuildRequires:	pandoc

%description
zbackup is a globally-deduplicating backup tool, based on the ideas
found in rsync. Feed a large .tar into it, and it will store duplicate
regions of it only once, then compress and optionally encrypt the
result. Feed another .tar file, and it will also re-use any data found
in any previous backups. This way only new changes are stored, and as
long as the files are not very different, the amount of storage
required is very low.

%prep
%setup -q

%build
%{__mkdir} -p objdir tartool/objdir
pushd objdir
%cmake ..
%{__make} %{?_smp_mflags}
popd
pushd tartool/objdir
%cmake ..
%{__make} %{?_smp_mflags}

%install
%{__make} install -C objdir DESTDIR=%{buildroot}
%{__install} tartool/objdir/tartool %{buildroot}%{_bindir}/
pandoc -s -f markdown_github -t man -V title=%{name} -V section=1 -V date="$(LANG=C date -d @$(stat -c'%Z' README.md) +'%B %d, %Y')" README.md -o %{name}.1
%{__install} -D -m 644 %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
ln -s %{name}.1 %{buildroot}%{_mandir}/man1/tartool.1

%files
%{_bindir}/*
%{_mandir}/man1/*.1.*
%license LICENSE*

%changelog
* Thu Dec 12 2014 Vladimir Stackov <amigo.elite at gmail dot com> - 1.3-3
- Produce hardened binaries

* Thu Dec 11 2014 Vladimir Stackov <amigo.elite at gmail dot com> - 1.3-2
- Modified in appliance with https://bugzilla.redhat.com/show_bug.cgi?id=1172525#c1
- Added tartool

* Wed Dec 10 2014 Vladimir Stackov <amigo.elite at gmail dot com> - 1.3-1
- Initial version of the package
