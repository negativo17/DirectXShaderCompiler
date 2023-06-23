%global date 20230623
%global commit0 60719ebc654d48ee3c017697f302fa8565691f9b
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global commit1 980971e835876dc0cde415e8f9bc646e64667bf7
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global commit2 268a061764ee69f09a477a695bf6a11ffe311b8d
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global commit3 23cb9b96cc2acf93e55839136b2c9643cbef6df6
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global commit4 66edefd2bb641de8a2f46b476de21f227fc03a28
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global commit5 b76a3eac1dfc7f0fe1d6a64cb59eab868056f099
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})

%global _warning_options -Wall -Werror=format-security -Wno-error=restrict

Name:           DirectXShaderCompiler
Version:        1.8.2306
Release:        1%{!?tag:.%{date}git%{shortcommit0}}%{?dist}
Summary:        DirectX Shader Compiler
License:        NCSA
URL:            https://github.com/microsoft/DirectXShaderCompiler

%if 0%{?tag:1}
Source0:        %url/archive/%{version}/%{name}-%{version}.tar.gz
%else
Source0:        %url/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%endif
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
%if 0%{?tag:1}
%autosetup -p1
%else
%autosetup -p1 -n %{name}-%{commit0}
%endif

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
* Fri Jun 23 2023 Simone Caronni <negativo17@gmail.com> - 1.8.2306-1.20230623git60719eb
- Update to 1.8.2306-preview branch snapshot (fixes build on Fedora 38).

* Sun Apr 02 2023 Simone Caronni <negativo17@gmail.com> - 1.7.2212.1-1
- First build.
