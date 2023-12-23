# vim: sw=4:ts=4:et

%define selinux_policyver 0.0.0

Name:   certadm_selinux
Version:	1.0
Release:	1%{?dist}
Summary:	SELinux policy module for certadm

Group:	System Environment/Base		
License:	GPLv2+	
# This is an example. You will need to change it.
URL:		http://HOSTNAME
Source0:	certadm.pp
Source1:	certadm.if
Source2:	certadm_selinux.8
Source3:	certadm_u

Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils
Requires(postun): policycoreutils
BuildArch: noarch

%description
This package installs and sets up the  SELinux policy security module for certadm.

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8/certadm_selinux.8
install -d %{buildroot}/etc/selinux/targeted/contexts/users/
install -m 644 %{SOURCE3} %{buildroot}/etc/selinux/targeted/contexts/users/certadm_u

%post
semodule -n -i %{_datadir}/selinux/packages/certadm.pp
# Add the new user defined in certadm_u only when the package is installed (not during updates)
if [ $1 -eq 1 ]; then
    /usr/sbin/semanage user -a -R certadm_r certadm_u
fi
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    
fi;
exit 0

%postun
if [ $1 -eq 0 ]; then
    /usr/sbin/semanage user -d certadm_u
    semodule -n -r certadm
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       
    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/certadm.pp
%{_datadir}/selinux/devel/include/contrib/certadm.if
%{_mandir}/man8/certadm_selinux.8.*
/etc/selinux/targeted/contexts/users/certadm_u

%changelog
* Sat Dec 23 2023 YOUR NAME <YOUR@EMAILADDRESS> 1.0-1
- Initial version

