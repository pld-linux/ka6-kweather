#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.04.0
%define		kframever	6.13.0
%define		qtver		6.8
%define		kaname		kweather
Summary:	KWeather
Name:		ka6-%{kaname}
Version:	25.04.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	c85d775c56a369e84d56606917846a25
URL:		http://www.kde.org/
BuildRequires:	Qt6Charts-devel >= %{qtver}
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Qml-devel
BuildRequires:	Qt6Test-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	gettext-tools
BuildRequires:	ka6-kweathercore-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kirigami-addons-devel >= 0.11.0
BuildRequires:	kf6-kirigami-devel >= %{kframever}
BuildRequires:	kf6-knotifications-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	python3
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Obsoletes:	ka5-%{kaname} < %{version}
Conflicts:	kde4-libksane >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A convergent weather application for Plasma.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kweather
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/applets/plasma_applet_kweather_1x4.so
%{_desktopdir}/org.kde.kweather.desktop
%{_datadir}/dbus-1/services/org.kde.kweather.service
%{_iconsdir}/hicolor/scalable/apps/org.kde.kweather.svg
%{_datadir}/metainfo/org.kde.kweather.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.kweather_1x4.appdata.xml
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.kweather_1x4
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.kweather_1x4/contents
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.kweather_1x4/contents/ui
%{_datadir}/plasma/plasmoids/org.kde.plasma.kweather_1x4/contents/ui/LocationSelector.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.kweather_1x4/contents/ui/WeatherContainer.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.kweather_1x4/contents/ui/main.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.kweather_1x4/metadata.json
%{_datadir}/plasma/plasmoids/org.kde.plasma.kweather_1x4/metadata.json.license
