Summary:	Boost 
Name:		boost
Version:	1.56.0
Release:	2%{?dist}
License:	Boost Software License V1
URL:		http://www.boost.org/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://downloads.sourceforge.net/boost/boost_1_56_0.tar.bz2
%define sha1 boost=f94bb008900ed5ba1994a1072140590784b9b5df
BuildRequires:	bzip2-devel

%description
Boost provides a set of free peer-reviewed portable C++ source libraries. It includes libraries for 
linear algebra, pseudorandom number generation, multithreading, image processing, regular expressions and unit testing.

%package        devel
Summary:        Development files for boost
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The boost-devel package contains libraries, header files and documentation
for developing applications that use boost.

%prep
%setup -qn boost_1_56_0
%build
./bootstrap.sh --prefix=%{buildroot}%{_prefix}
./b2 %{?_smp_mflags} stage threading=multi link=shared
%install
./b2 install threading=multi link=shared
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/*.so

%files devel
%{_libdir}/*.a
%{_includedir}/*

%changelog
*	Thu Oct 01 2015 Xiaolin Li <xiaolinl@vmware.com> 1.56.0-2
_	Move header files to devel package.
*	Tue Feb 10 2015 Divya Thaluru <dthaluru@vmware.com> 1.56.0-1
-	Initial build.	First version
