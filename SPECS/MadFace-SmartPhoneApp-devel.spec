Summary: MadFace-SmartPhoneApp-devel
Name: MadFace-SmartPhoneApp-devel
Version: 0.2.0
Release: 20171023
License: Apache License Version 2.0
Group: System Environment/Daemons
#Source0: MadFaceSmartPhoneApp.zip
Source0: android_sdk.sh
BuildRoot: %{_tmppath}/%{name}-%{version}-root
AutoReqProv: no
Requires: MadFace
Requires: npm
Requires: nodejs
Requires: java-1.7.0-openjdk-devel
Requires: ant-apache-regexp



######################################################################
#
#
# Preamble
#
# Macro definitions
#%define _branch_name  201608
#%define _source_dir     MadFaceSmartPhoneApp-%{_branch_name}


%define _prefix         /usr/lib/
%define _profile_dir    /etc/profile.d

%define madface_uid   374
%define madface_user  madface
%define madface_gid   374
%define madface_group madface


%description
HappyFace is a powerful site specific monitoring system for data from multiple input sources. This system collects, processes, rates and presents all important monitoring information for the overall status and the services of a local or Grid computing site. 


%prep
#%setup -q -n %{_source_dir}

%build
#make

%install
cd ..

[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# make directories
! [ -d $RPM_BUILD_ROOT/%{_prefix} ] && mkdir -vp $RPM_BUILD_ROOT/%{_prefix}
! [ -d $RPM_BUILD_ROOT/%{_profile_dir} ] && mkdir -vp $RPM_BUILD_ROOT/%{_profile_dir}


## Android development env
ANT="https://archive.apache.org/dist/ant/binaries/apache-ant-1.9.5-bin.zip"
ADT="https://dl.google.com/android/adt/adt-bundle-linux-x86_64-20140702.zip"
[ ! -e /tmp/$(basename $ANT) ] && wget "$ANT" -O /tmp/$(basename $ANT)
[ ! -e /tmp/$(basename $ADT) ] && wget "$ADT" -O /tmp/$(basename $ADT)

[ ! -e $RPM_BUILD_ROOT/%{_prefix}/apache-ant ] && unzip /tmp/$(basename $ANT) -d $RPM_BUILD_ROOT/%{_prefix} && ln -s %{_prefix}/apache-ant-1.9.5 $RPM_BUILD_ROOT/%{_prefix}/apache-ant
[ ! -e $RPM_BUILD_ROOT/%{_prefix}/android ] && unzip /tmp/$(basename $ADT) -d $RPM_BUILD_ROOT/%{_prefix} && ln -s %{_prefix}/adt-bundle-linux-x86_64-20140702 $RPM_BUILD_ROOT/%{_prefix}/android

cp -v %{SOURCE0} $RPM_BUILD_ROOT/%{_profile_dir}/




%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%pre

%post


%files
%defattr(-,madface,madface)
%{_prefix}/apache-ant
%{_prefix}/apache-ant-1.9.5
%{_prefix}/android
%{_prefix}/adt-bundle-linux-x86_64-20140702

%defattr(-,root,root)
%{_profile_dir}/android_sdk.sh




%changelog
* Mon Oct 23 2017 Gen Kawamura <Gen.Kawamura@cern.ch> 0.3.0-1
- For RHEL7
* Tue Jul 09 2015 Gen Kawamura <Gen.Kawamura@cern.ch> 0.0.1-20150611
- initial packaging
