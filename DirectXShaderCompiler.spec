%global commit1 980971e835876dc0cde415e8f9bc646e64667bf7
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global commit2 1d31a100405cf8783ca7a31e31cdd727c9fc54c3
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global commit3 40f5bf59c6acb4754a0bffd3c53a715732883a12
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global commit4 35912e1b7778ec2ddcff7e7188177761539e59e0
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global commit5 4be240789d5b322df9f02b7e19c8651f3ccbf205
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})

%global _warning_options -Wall -Werror=format-security -Wno-error=restrict

Name:           DirectXShaderCompiler
Version:        1.7.2212.1
Release:        1%{?dist}
Summary:        DirectX Shader Compiler
License:        NCSA
URL:            https://github.com/microsoft/DirectXShaderCompiler

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/microsoft/DirectX-Headers/archive/%{commit1}.tar.gz#/DirectX-Headers-%{shortcommit1}.tar.gz
Source2:        https://github.com/KhronosGroup/SPIRV-Headers/archive/%{commit2}.tar.gz#/SPIRV-Headers-%{shortcommit2}.tar.gz
Source3:        https://github.com/KhronosGroup/SPIRV-Tools/archive/%{commit3}.tar.gz#/SPIRV-Tools-%{shortcommit3}.tar.gz
Source4:        https://github.com/google/effcee/archive/%{commit4}.tar.gz#/effcee-%{shortcommit4}.tar.gz
Source5:        https://github.com/google/re2/archive/%{commit5}.tar.gz#/re2-%{shortcommit5}.tar.gz

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
tar -xzf %{SOURCE4} --strip-components=1 -C external/effcee
tar -xzf %{SOURCE5} --strip-components=1 -C external/re2

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
install -m755 %{_vpath_builddir}/bin/dxc* %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_libdir}
install -m755 %{_vpath_builddir}/lib/libdxcompiler.so \
    %{buildroot}%{_libdir}/
install -m644 %{_vpath_builddir}/lib/libdxclib.a \
    %{buildroot}%{_libdir}/

mkdir -p %{buildroot}%{_includedir}/dxc
install -m644 include/dxc/{dxcapi.h,dxcerrors.h,dxcisense.h,WinAdapter.h} \
    %{buildroot}%{_includedir}/dxc/

%files
%license LICENSE.TXT
%doc CONTRIBUTING.md README.md SECURITY.md ThirdPartyNotices.txt
%{_bindir}/dxc
%{_bindir}/dxc-3.7
%{_includedir}/dxc
%{_libdir}/libdxcompiler.so
%{_libdir}/libdxclib.a

%changelog
* Sun Apr 02 2023 Simone Caronni <negativo17@gmail.com> - 1.7.2212.1-1
- First build.
