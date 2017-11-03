Summary: MadFace
Name: MadFace
Version: 0.2.0
Release: 1
License: GPL
Group: System Environment/Daemons
URL: http://goegrid-controller.ph2.physik.uni-goettingen.de:8111
#Source0: ftp://rpm.org/%{name}_%{version}.source.tar.gz
Source0: %{name}-%{version}.tar.gz
Source1: MadFace-R-libs-%{version}.tar.gz
#BuildPreReq: python
BuildRoot: %{_tmppath}/%{name}-%{version}-root
AutoReqProv: no

Requires: xorg-x11-server-Xvfb
Requires: nodejs
Requires: npm
Requires: tmpwatch
Requires: firefox
Requires: docker-io
Requires: ImageMagick
Requires: festival
Requires: xdotool
Requires: jq
Requires: fftw-devel
Requires: fftw2-devel
Requires: festival
Requires: festvox-ked-diphone
Requires: festvox-kal-diphone
Requires: festvox-slt-arctic-hts
Requires: festvox-bdl-arctic-hts
Requires: festvox-rms-arctic-hts
Requires: festvox-awb-arctic-hts
Requires: festvox-clb-arctic-hts
Requires: festvox-jmk-arctic-hts

%package R-libs
Summary: R libraries used for MadFace analyzer
Group: Applications/Engineering
Version: %{version}
Requires: R >= 3.3.0
BuildRequires: fftw-devel
BuildRequires: fftw2-devel
BuildRequires: libjpeg-turbo
BuildRequires: libjpeg-turbo-devel


######################################################################
#
#
# Preamble
#
# Macro definitions
%define _prefix         /usr/lib
%define _etc            /etc
%define _profile_dir    /etc/profile.d
%define _datadir        /var/lib/MadFace
%define _logdir         /var/log/MadFace
%define _piddir         /var/run/MadFace
%define _Rlibdir        /usr/lib64/R/library

%define madface_uid   374
%define madface_user  madface
%define madface_gid   374
%define madface_group madface


%description
MadFace is a powerful monitoring application running on both PC and Smartphone platforms.

%description R-libs
MadFace R libraries


%prep
%setup -q -b 0 -n %{name}
%setup -q -b 1 -n MadFace-R-libs

%build

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
[ ! -d $RPM_BUILD_ROOT/%{_prefix} ] && mkdir -p $RPM_BUILD_ROOT/%{_prefix}
[ ! -d $RPM_BUILD_ROOT/%{_etc} ] && mkdir -p $RPM_BUILD_ROOT/%{_etc}
[ ! -d $RPM_BUILD_ROOT/%{_datadir} ] && mkdir -p $RPM_BUILD_ROOT/%{_datadir}
[ ! -d $RPM_BUILD_ROOT/%{_logdir} ] && mkdir -p $RPM_BUILD_ROOT/%{_logdir}
[ ! -d $RPM_BUILD_ROOT/%{_piddir} ] && mkdir -p $RPM_BUILD_ROOT/%{_piddir}
[ ! -d $RPM_BUILD_ROOT/%{_Rlibdir} ] && mkdir -p $RPM_BUILD_ROOT/%{_Rlibdir}
cd ..

## package
cp -vr %{name} $RPM_BUILD_ROOT/%{_prefix}


## configuration
[ ! -d $RPM_BUILD_ROOT/%{_etc}/rc.d/init.d ] && mkdir -p $RPM_BUILD_ROOT/%{_etc}/rc.d/init.d

MADFACE_HOME=%{_prefix}/MadFace
mv -v $RPM_BUILD_ROOT/%{_prefix}/MadFace/daemon/madface.conf $RPM_BUILD_ROOT/%{_etc}/madface.conf
mv -v $RPM_BUILD_ROOT/%{_prefix}/MadFace/daemon/madfaced $RPM_BUILD_ROOT/%{_etc}/rc.d/init.d/
rmdir -v $RPM_BUILD_ROOT/%{_prefix}/MadFace/daemon
rm -v $RPM_BUILD_ROOT/%{_prefix}/MadFace/data
ln -s %{_datadir} $RPM_BUILD_ROOT/%{_prefix}/MadFace/data


## R library
for p in $(cat MadFace-R-libs/packages-3.3.0/packages.txt)
do
	echo "Compiling [$p] ..."
	/usr/bin/R CMD INSTALL -c -l $RPM_BUILD_ROOT/%{_Rlibdir} MadFace-R-libs/packages-3.3.0/$p
done



%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%pre
echo "Creating new user [madface] ..."
groupadd -r %{madface_group} -g %{madface_gid}
useradd -r %{madface_user} -c 'MadFace System' -u %{madface_uid} -g %{madface_group} -g dockerroot -d %{_prefix}/MadFace -M


%post
echo "Setting up Ionic and Cordova"
which cordova || npm install -g cordova@5.1.1
if ! which ionic; then
    npm install -g ionic@1.6.1
    WRONG_FILE=/usr/lib/node_modules/ionic/node_modules/ionic-app-lib/lib/config.js
    cat $WRONG_FILE | perl -pe "s/CONFIG_FILE:.*/CONFIG_FILE: \'.\/ionic\/ionic.config\',/g" > /tmp/config.js
    cp -v /tmp/config.js $WRONG_FILE
fi
which jpm || npm install -g jpm@1.0.7
which forever || npm install -g forever@0.15.2


%postun
echo "Deleting user [madface]..."
pids=$(ps aux | grep "^madface" | awk '{print $2}')
[ ! -z "$pids" ] && kill -kill $pids
sleep 1

userdel %{madface_user}
groupdel %{madface_group}


%files
%defattr(-,madface,madface)
%{_prefix}/MadFace
%{_datadir}
%{_logdir}
%{_piddir}
%defattr(-,root,root)
%{_etc}/*

%files R-libs
%defattr(-,root,root)
%{_Rlibdir}

%changelog
* Mon Oct 23 2017 Gen Kawamura <Gen.Kawamura@cern.ch> 0.3.0-1
- For RHEL7
* Mon Aug 01 2016 Gen Kawamura <Gen.Kawamura@cern.ch> 0.2.0-4
- Added some patches
* Mon Aug 01 2016 Gen Kawamura <Gen.Kawamura@cern.ch> 0.2.0-3
- Added R libraries in RPM
* Thu Jul 07 2016 Gen Kawamura <Gen.Kawamura@cern.ch> 0.2.0-2
- Added a runnable daemon
* Thu May 26 2016 Gen Kawamura <Gen.Kawamura@cern.ch> 0.2.0-1
- initial packaging

