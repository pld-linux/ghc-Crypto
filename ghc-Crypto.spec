#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	Crypto
Summary:	Collects together existing Haskell cryptographic functions into a package
Summary(pl.UTF-8):	Zebranie istniejących funkcji kryptograficznych Haskella w pakiet
Name:		ghc-%{pkgname}
Version:	4.2.5.1
Release:	5
License:	BSD, GPL v2+ (depending on module)
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/Crypto
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	e1ec7d91e888107f2544064456f8eb36
URL:		http://hackage.haskell.org/package/Crypto
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-HUnit
BuildRequires:	ghc-QuickCheck >= 2.4.0.1
BuildRequires:	ghc-array
BuildRequires:	ghc-base >= 3
BuildRequires:	ghc-pretty
BuildRequires:	ghc-random
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-HUnit-prof
BuildRequires:	ghc-QuickCheck-prof >= 2.4.0.1
BuildRequires:	ghc-array-prof
BuildRequires:	ghc-base-prof >= 3
BuildRequires:	ghc-pretty-prof
BuildRequires:	ghc-random-prof
%endif
BuildRequires:	latex2html
BuildRequires:	texlive-format-pdflatex
BuildRequires:	texlive-latex
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-array
Requires:	ghc-base >= 3
Requires:	ghc-pretty
Requires:	ghc-random
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
DES, Blowfish, AES, TEA, SHA1, MD5, RSA, BubbleBabble, Hexdump,
support for Word128, Word192 and Word256 and beyond, PKCS5 padding,
various encryption modes e.g. Cipher Block Chaining all in one
package, with HUnit and QuickCheck tests, and examples.

%description -l pl.UTF-8
DES, Blowfish, AES, TEA, SHA1, MD5, RSA, BubbleBabble, Hexdump,
obsługa typów Word128, Word192, Word256 i dalszych, opakowania PKCS5,
różnych trybów szyfrowania, jak CBC (Cipher Block Chaining) - wszystko
w jednym pakiecie, wraz z testami HUnit i QuickCheck oraz przykładami.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-array-prof
Requires:	ghc-base-prof >= 3
Requires:	ghc-pretty-prof
Requires:	ghc-random-prof

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
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
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%{__rm} $RPM_BUILD_ROOT%{_bindir}/{HMAC,Quick,RSA,SHA1,Symmetric,WordList}Test
%{__rm} $RPM_BUILD_ROOT%{_datadir}/Crypto-%{version}/CryptoHomePage.html

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CryptoHomePage.html ReadMe.pdf %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSCrypto-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSCrypto-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSCrypto-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Binary
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Binary/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Binary/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Encryption
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Encryption/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Encryption/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Encryption/RSA
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Encryption/RSA/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Encryption/RSA/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Text
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Text/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Text/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Digest
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Digest/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Digest/*.dyn_hi

%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSCrypto-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Binary/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Encryption/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Encryption/RSA/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Text/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Digest/*.p_hi
