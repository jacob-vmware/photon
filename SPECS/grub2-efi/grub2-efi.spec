%define debug_package %{nil}
%define __os_install_post %{nil}
Summary:	GRand Unified Bootloader
Name:		grub2-efi
Version:	2.02
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/grub
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://alpha.gnu.org/gnu/grub/grub-2.02~beta2.tar.gz
%define sha1 grub=b2c9227f9a54587532ae3f727d197ab112cdbbb3
BuildRequires:	device-mapper-devel
BuildRequires:	xz-devel
Requires:	xz
Requires:	device-mapper
%description
The GRUB package contains the GRand Unified Bootloader.

%package lang
Summary: Additional language files for grub
Group: System Environment/Programming
Requires: grub2 >= 2.00
%description lang
These are the additional language files of grub.


%prep
%setup -qn grub-2.02~beta2
#sed -i -e '/gets is a/d' grub-core/gnulib/stdio.in.h
%build

./configure \
	--prefix=%{_prefix} \
	--sbindir=/sbin \
	--sysconfdir=%{_sysconfdir} \
	--disable-grub-emu-usb \
	--disable-werror \
    --disable-efiemu \
	--program-transform-name=s,grub,%{name}, \
	--with-grubdir=grub2 \
    --with-platform=efi \
    --target=x86_64 \
    --with-program-prefix="" \
    --with-bootdir="/boot" 

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
mkdir %{buildroot}%{_sysconfdir}/default
touch %{buildroot}%{_sysconfdir}/default/grub
mkdir %{buildroot}%{_sysconfdir}/sysconfig
ln -sf %{_sysconfdir}/default/grub %{buildroot}%{_sysconfdir}/sysconfig/grub
mkdir -p %{buildroot}/boot/%{name}
touch %{buildroot}/boot/%{name}/grub.cfg
rm -rf %{buildroot}%{_infodir}
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%dir %{_sysconfdir}/grub.d
%config() %{_sysconfdir}/bash_completion.d/grub
%config() %{_sysconfdir}/grub.d/00_header
%config() %{_sysconfdir}/grub.d/10_linux
%config() %{_sysconfdir}/grub.d/20_linux_xen
%config() %{_sysconfdir}/grub.d/30_os-prober
%config() %{_sysconfdir}/grub.d/40_custom
%config() %{_sysconfdir}/grub.d/41_custom
%config() %{_sysconfdir}/grub.d/README
/sbin/*
%{_bindir}/*
%{_libdir}/grub/*
%{_datarootdir}/grub/*
%{_sysconfdir}/sysconfig/grub
%{_sysconfdir}/default/grub
%ghost %config(noreplace) /boot/%{name}/grub.cfg

%files lang
%defattr(-,root,root)
/usr/share/locale/*

%changelog
*	Fri Jul 31 2015 Sharath George <sharathg@vmware.com> 2.02-1
-	Adding EFI support.
