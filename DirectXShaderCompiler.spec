# external/DirectX-Headers
%global commit1 980971e835876dc0cde415e8f9bc646e64667bf7
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
# external/SPIRV-Headers
%global commit2 1c6bb2743599e6eb6f37b2969acc0aef812e32e3
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
# external/SPIRV-Tools
%global commit3 f0cc85efdbbe3a46eae90e0f915dc1509836d0fc
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})

%global _warning_options -Wall -Werror=format-security -Wno-error=restrict

Name:           DirectXShaderCompiler
Version:        1.8.2403.2
Release:        1%{?dist}
Summary:        DirectX Shader Compiler
License:        NCSA
URL:            https://github.com/microsoft/DirectXShaderCompiler

Source0:        %url/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/microsoft/DirectX-Headers/archive/%{commit1}.tar.gz#/DirectX-Headers-%{shortcommit1}.tar.gz
Source2:        https://github.com/KhronosGroup/SPIRV-Headers/archive/%{commit2}.tar.gz#/SPIRV-Headers-%{shortcommit2}.tar.gz
Source3:        https://github.com/KhronosGroup/SPIRV-Tools/archive/%{commit3}.tar.gz#/SPIRV-Tools-%{shortcommit3}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git-core
BuildRequires:  llvm-devel
BuildRequires:  libxml2-devel
BuildRequires:  ninja-build
BuildRequires:  python3-devel

Provides:       dxc = %{version}-%{release}

%description
The DirectX Shader Compiler project includes a compiler and related tools used
to compile High-Level Shader Language (HLSL) programs into DirectX Intermediate
Language (DXIL) representation. Applications that make use of DirectX for
graphics, games, and computation can use it to generate shader programs.

%prep
%autosetup -p1

tar -xzf %{SOURCE1} --strip-components=1 -C external/DirectX-Headers
tar -xzf %{SOURCE2} --strip-components=1 -C external/SPIRV-Headers
tar -xzf %{SOURCE3} --strip-components=1 -C external/SPIRV-Tools

%build
%cmake \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_BUILD_TYPE=Fedora \
    -DCMAKE_C_COMPILER=gcc \
    -DCMAKE_CXX_COMPILER=g++ \
    -DSPIRV_BUILD_TESTS=OFF \
    -C cmake/caches/PredefinedParams.cmake

%cmake_build

%install
mkdir -p %{buildroot}%{_bindir}
install -m755 %{_vpath_builddir}/bin/dx{a,c,l,opt,r,v}* \
    %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_libdir}
install -m755 %{_vpath_builddir}/lib/libdxcompiler.so \
    %{buildroot}%{_libdir}/
install -m644 %{_vpath_builddir}/lib/libdxclib.a \
    %{buildroot}%{_libdir}/

mkdir -p %{buildroot}%{_includedir}/dxc
install -m644 include/dxc/*.h \
    %{buildroot}%{_includedir}/dxc/

%files
%license LICENSE.TXT
%doc CONTRIBUTING.md README.md SECURITY.md ThirdPartyNotices.txt
%{_bindir}/dxa
%{_bindir}/dxa-3.7
%{_bindir}/dxc
%{_bindir}/dxc-3.7
%{_bindir}/dxl
%{_bindir}/dxl-3.7
%{_bindir}/dxopt
%{_bindir}/dxopt-3.7
%{_bindir}/dxr
%{_bindir}/dxr-3.7
%{_bindir}/dxv
%{_bindir}/dxv-3.7
%{_includedir}/dxc
%{_libdir}/libdxcompiler.so
%{_libdir}/libdxclib.a

%changelog
* Tue Apr 02 2024 Simone Caronni <negativo17@gmail.com> - 1.8.2403.2-1
- Update to 1.8.2403.2 (patch 2).
- Clean up SPEC file.

* Tue Mar 12 2024 Simone Caronni <negativo17@gmail.com> - 1.8.2403-2
- Update to final 1.8.2403 release.

* Sun Feb 18 2024 Simone Caronni <negativo17@gmail.com> - 1.8.2403-1.20240217gitc80232c
- Update to snapshot of 1.8.2403 release.

* Fri Jun 23 2023 Simone Caronni <negativo17@gmail.com> - 1.8.2306-1.20230623git60719eb
- Update to 1.8.2306-preview branch snapshot (fixes build on Fedora 38).

* Sun Apr 02 2023 Simone Caronni <negativo17@gmail.com> - 1.7.2212.1-1
- First build.
