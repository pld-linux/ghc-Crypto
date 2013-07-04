%define		pkgname	Crypto
Summary:	Collects together existing Haskell cryptographic functions into a package
Name:		ghc-%{pkgname}
Version:	4.2.5.1
Release:	1
License:	BSD / GPL
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/%{pkgname}/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	e1ec7d91e888107f2544064456f8eb36
URL:		http://hackage.haskell.org/package/Crypto/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-HUnit
BuildRequires:	ghc-QuickCheck
BuildRequires:	ghc-prof
BuildRequires:	latex2html
BuildRequires:	texlive-format-pdflatex
BuildRequires:	texlive-latex
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_releq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
#Requires:	ghc-OTHERMODULE
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddoc files
%define		_noautocompressdoc	*.haddock

%description
DES, Blowfish, AES, TEA, SHA1, MD5, RSA, BubbleBabble, Hexdump,
Support for Word128, Word192 and Word256 and Beyond, PKCS5 Padding,
Various Encryption Modes e.g. Cipher Block Chaining all in one
package, with HUnit and QuickCheck tests, and examples.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 --enable-library-profiling \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

pdflatex ReadMe.tex

cd dist/build
for f in *Test ; do
	$f/$f
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CryptoHomePage.html ReadMe.pdf
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Binary
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Encryption
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Encryption/RSA
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Text
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Digest
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Binary/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Encryption/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Encryption/RSA/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Text/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Digest/*.hi

%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Binary/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Encryption/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Encryption/RSA/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Text/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Digest/*.p_hi
