%if 0%{?fedora}
%global debug_package %{nil}
%endif

Name:     vangogh_oc_fix
Version:  {{{ git_dir_version }}}
Release:  1%{?dist}
Summary:  A linux kernel module to override AMD Van Gogh APU PowerPlay limits for CPU
License:  GPLv3
URL:      https://github.com/KyleGospo/vangogh_oc_fix-kmod/

Source:   %{url}/archive/refs/heads/main.tar.gz

Provides: %{name}-kmod-common = %{version}
Requires: %{name}-kmod >= %{version}

BuildRequires: systemd-rpm-macros

%description
A linux kernel module to override AMD Van Gogh APU PowerPlay limits for CPU. This is useful if you have overclocked your SteamDeck but still want to use PowerTools to set CPU clock limits. You do not need this for GPU overclocking.

Note that you still need a pt_oc.json to tell PowerTools that it can go that hard. Conservesly, the way PowerTools works as of writing this (2023-03-06) will not go past stock settings even if you have a pt_oc.json but not this module. Similarly, you still need to set your maximum clock speed through the BIOS, either through SmokelessUMAF or SD_Unlocker depending on your BIOS version.

%prep
%setup -q -c vangogh_oc_fix-kmod-main

%files
%doc vangogh_oc_fix-kmod-main/README.md
%license vangogh_oc_fix-kmod-main/LICENSE

%changelog
{{{ git_dir_changelog }}}
