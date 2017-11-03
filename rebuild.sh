#!/bin/sh

usage="[$0] [sync|build|ctest|apply]"
[ $# -eq 0 ] && echo "$usage" && exit 0

case $1 in
    sync)
	cd SOURCES
	rsync -alvp --delete --exclude .git --exclude .git.local --exclude platforms/android/build ~/var/develop/goegrid-admin-interface/madface .
	rsync -alvp --delete --exclude .git --exclude .git.local ~/var/develop/docker-containers/R-madface.el6 .
	rm -rf MadFace MadFace-R-libs
	mv -v madface MadFace
	mv -v R-madface.el6 MadFace-R-libs
	tar --exclude-vcs -zcvf MadFace-0.3.0.tar.gz MadFace
	tar --exclude-vcs -zcvf MadFace-R-libs-0.3.0.tar.gz MadFace-R-libs
	cd ..
	;;
    build)
        ## create .rpmmacros
	echo "%_topdir        $PWD" > rpmmacros_MadFace
	ln -sf $PWD/rpmmacros_MadFace ~/.rpmmacros
	specs="MadFace.spec"
	if [ ! -z "$2" ]; then
	    case $2 in
		android)
		    specs="MadFace-SmartPhoneApp-devel.spec"
		    ;;
		madface)
		    specs="MadFace.spec"
		    ;;
	    esac
	fi
	rpmbuild --define 'dist .el7' --clean -ba SPECS/$specs
	;;
    install)
	yum -y --nogpgcheck install epel-release
	yum -y --nogpgcheck install RPMS/MadFace-latest.x86_64.rpm RPMS/MadFace-R-libs-latest.x86_64.rpm
	;;
    ctest)
	echo "Installing in a docker container"
	docker run -v $PWD:/root -w /root -it centos:6 ./rebuild.sh install
	docker rmi $(docker ps -a -q)
	;;
    apply)
	login=login.ph2.physik.uni-goettingen.de
	mad_host=goegrid-controller
	rsync -avzL --delete -e "ssh -o \"ProxyCommand ssh -W %h:%p -p 24 gen@${login}\"" RPMS/*.rpm goegrid@$mad_host:/tmp
	if [ ! -z "$2" ]; then
	    case $2 in
		android)
		    ssh -t -p 24 gen@$login ssh -t root@$mad_host "'yum -y remove MadFace-SmartPhoneApp-devel; yum --nogpgcheck -y install /tmp/MadFace-SmartPhoneApp-devel-latest.x86_64.rpm'"
		    ;;
		madface)
		    ssh -t -p 24 gen@$login ssh -t root@$mad_host "'yum -y remove MadFace MadFace-R-libs; yum --nogpgcheck -y install /tmp/MadFace-latest.x86_64.rpm /tmp/MadFace-R-libs-latest.x86_64.rpm && rm -vf /var/run/MadFace/ionic*; /etc/init.d/madfaced start'"
		    ;;
	    esac
	fi
	;;
	
    *)
	echo "$usage"
	exit -1
	;;
esac
