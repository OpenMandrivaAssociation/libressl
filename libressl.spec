%define cryptomajor 38
%define sslmajor 39
%define tlsmajor 11

%define libcrypto %{mklibname crypto %{cryptomajor}}
%define cryptodev %{mklibname crypto -d}
%define libssl %{mklibname ssl %{sslmajor}}
%define ssldev %{mklibname ssl -d}
%define libtls %{mklibname tls %{tlsmajor}}
%define tlsdev %{mklibname tls -d}

Name: libressl
Version: 2.4.2
Release: 1
Source0: http://ftp.openbsd.org/pub/OpenBSD/LibreSSL/%{name}-%{version}.tar.gz
Summary: Secure Sockets Layer communications libs & utils
URL: https://libressl.org/
License: BSD-like
Group: System/Libraries
%rename openssl

%description
The openssl certificate management tool and the shared libraries that provide
various encryption and decription algorithms and protocols, including DES, RC4,
RSA and SSL.

%package -n %{libcrypto}
Summary: Libressl cryptography library
Group: System/Libraries
# Compatibility with OpenSSL
%if "%{_lib}" == "lib64"
Provides: libcrypto.so.1.0.0()(64bit)
%else
Provides: libcrypto.so.1.0.0
%endif
%rename %{_lib}crypto1.0.0

%description -n %{libcrypto}
The openssl certificate management tool and the shared libraries that provide
various encryption and decription algorithms and protocols, including DES, RC4,
RSA and SSL.

%files -n %{libcrypto}
/%{_lib}/libcrypto.so.%{cryptomajor}*
/%{_lib}/libcrypto.so.1.0.0

%package -n %{cryptodev}
Summary: Development files for the libressl crypto library
Group: Development/Other
Requires: %{libcrypto} = %{EVRD}

%description -n %{cryptodev}
Development files for the libressl crypto library

%files -n %{cryptodev} -f cryptodev.list
%dir %{_includedir}/openssl
%{_includedir}/openssl/opensslfeatures.h
/%{_lib}/libcrypto.so
%{_libdir}/libcrypto.so
%{_libdir}/pkgconfig/libcrypto.pc
%{_mandir}/man3/*

%package -n %{libssl}
Summary: Libressl SSL/TLS library
Group: System/Libraries
# Compatibility with OpenSSL
%if "%{_lib}" == "lib64"
Provides: libssl.so.1.0.0()(64bit)
%else
Provides: libssl.so.1.0.0
%endif
%rename %{_lib}ssl1.0.0

%description -n %{libssl}
The openssl certificate management tool and the shared libraries that provide
various encryption and decription algorithms and protocols, including DES, RC4,
RSA and SSL.

%files -n %{libssl}
/%{_lib}/libssl.so.%{sslmajor}*
/%{_lib}/libssl.so.1.0.0

%package -n %{ssldev}
Summary: Development files for the libressl ssl library
Group: Development/Other
Requires: %{libssl} = %{EVRD}
Requires: %{cryptodev} = %{EVRD}
Provides: openssl-devel = %{EVRD}
%rename lib64openssl-devel

%description -n %{ssldev}
Development files for the libressl SSL/TLS library

%files -n %{ssldev} -f ssldev.list
/%{_lib}/libssl.so
%{_libdir}/libssl.so
%{_libdir}/pkgconfig/libssl.pc
%{_libdir}/pkgconfig/openssl.pc
%{_includedir}/openssl/dtls1.h
%{_includedir}/openssl/ossl_typ.h
%{_includedir}/openssl/srtp.h
%{_includedir}/openssl/ssl2.h
%{_includedir}/openssl/ssl23.h
%{_includedir}/openssl/ssl3.h
%{_includedir}/openssl/tls1.h

%package -n %{libtls}
Summary: Libressl SSL/TLS library
Group: System/Libraries

%description -n %{libtls}
The openssl certificate management tool and the shared libraries that provide
various encryption and decription algorithms and protocols, including DES, RC4,
RSA and SSL.

%files -n %{libtls}
/%{_lib}/libtls.so.%{tlsmajor}*

%package -n %{tlsdev}
Summary: Development files for the libressl TLS library
Group: Development/Other
Requires: %{libtls} = %{EVRD}
Requires: %{ssldev} = %{EVRD}

%description -n %{tlsdev}
Development files for the libressl SSL/TLS library

%files -n %{tlsdev}
/%{_lib}/libtls.so
%{_libdir}/libtls.so
%{_libdir}/pkgconfig/libtls.pc
%{_includedir}/tls.h

%prep
%setup -q
%configure \
	--with-openssldir=%{_sysconfdir}/pki/tls \
	--libdir=/%{_lib} \

%build
%make

%install
%makeinstall_std
mkdir -p %{buildroot}%{_libdir}
mv %{buildroot}/%{_lib}/pkgconfig %{buildroot}%{_libdir}
ln -s ../../%{_lib}/libssl.so.%{sslmajor} %{buildroot}%{_libdir}/libssl.so
ln -s ../../%{_lib}/libcrypto.so.%{cryptomajor} %{buildroot}%{_libdir}/libcrypto.so
ln -s ../../%{_lib}/libtls.so.%{tlsmajor} %{buildroot}%{_libdir}/libtls.so

find %{buildroot}%{_includedir} -name "*.h" |while read r; do
	b="`basename $r`"
	if grep -qrE "#include.*/$b>" crypto; then
		echo %{_includedir}/openssl/$b >>cryptodev.list
	elif grep -qrE "#include.*/$b>" ssl; then
		echo %{_includedir}/openssl/$b >>ssldev.list
	fi
done

# For compatibility with OpenSSL
ln -sf libssl.so.%{sslmajor} %{buildroot}/%{_lib}/libssl.so.1.0.0
ln -sf libcrypto.so.%{cryptomajor} %{buildroot}/%{_lib}/libcrypto.so.1.0.0

%check
make check

%files
%{_bindir}/*
%{_mandir}/man1/*
%dir %{_sysconfdir}/pki/tls
%{_sysconfdir}/pki/tls/cert.pem
%{_sysconfdir}/pki/tls/openssl.cnf
%{_sysconfdir}/pki/tls/x509v3.cnf
