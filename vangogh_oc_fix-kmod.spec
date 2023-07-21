%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

Name:     vangogh_oc_fix-kmod
Version:  {{{ git_dir_version }}}
Release:  1%{?dist}
Summary:  A linux kernel module to override AMD Van Gogh APU PowerPlay limits for CPU
License:  GPLv3
URL:      https://github.com/KyleGospo/vangogh_oc_fix-kmod/

Source:   %{url}/archive/refs/heads/main.tar.gz
Source1:  https://raw.githubusercontent.com/badly-drawn-wizards/vangogh_oc_fix/master/module/vangogh_oc_fix.c

BuildRequires: kmodtool

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Driver exposing various bits and pieces of functionality provided by Steam Deck specific VLV0100 device presented by EC firmware.
This includes but not limited to:
- CPU/device's fan control
- Read-only access to DDIC registers
- Battery tempreature measurements
- Various display related control knobs
- USB Type-C connector event notification

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c vangogh_oc_fix-kmod-main
cp %{SOURCE1} vangogh_oc_fix-kmod-main/vangogh_oc_fix.c

find . -type f -name '*.c' -exec sed -i "s/#VERSION#/%{version}/" {} \+

for kernel_version  in %{?kernel_versions} ; do
  cp -a vangogh_oc_fix-kmod-main _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version  in %{?kernel_versions} ; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} VERSION=v%{version} modules
done

%install
for kernel_version in %{?kernel_versions}; do
 mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 install -D -m 755 _kmod_build_${kernel_version%%___*}/vangogh_oc_fix.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/vangogh_oc_fix.ko
done
%{?akmod_install}

%changelog
{{{ git_dir_changelog }}}
