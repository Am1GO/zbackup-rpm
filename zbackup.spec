Name:		zbackup
Version:	1.3
Release:	1%{?dist}
Summary:	A versatile deduplicating backup tool

Group:		Applications/Archiving
License:	GPLv2+ and OpenSSL
URL:		http://zbackup.org/
Source0:	https://github.com/zbackup/zbackup/archive/%{version}.tar.gz

BuildRequires:	cmake >= 2.8.2
BuildRequires:	xz-devel
BuildRequires:	openssl-devel
BuildRequires:	protobuf-devel
BuildRequires:	zlib-devel
BuildRequires:	pandoc
Requires:	xz-libs zlib protobuf openssl-libs

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
%{__install} -d objdir
cd objdir
%cmake ..
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install -C objdir DESTDIR=%{buildroot}
%{__mkdir} -p %{buildroot}%{_mandir}/man1/
pandoc -s -f markdown_github -t man -V title=%{name} -V section=1 -V date="$(LANG=C date -d @$(stat -c'%Z' README.md) +'%B %d, %Y')" README.md -o %{name}.1
%{__install} -m 644 %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%doc LICENSE*
%{_mandir}/man1/%{name}.1.gz

%changelog
* Wed Dec 10 2014 Vladimir Stackov <amigo.elite at gmail dot com> - 1.3.1
- Initial version of the package
