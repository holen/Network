#Install perl module

    yum install -y perl-CPAN
    perl -MCPAN -e shell
    install Net::DNS     
    install Sys::Syslog     
    install Data::Dumper     
    install Getopt::Long
    yum install gcc
    perl -MCPAN -e 'install Net::DNS'
    perl -MCPAN -e 'install Sys::Syslog'
    perl -MCPAN -e 'install Getopt::Long'
    perl -MCPAN -e 'install Data::Dumper'

Install ip 纯真库

    wget http://search.cpan.org/CPAN/authors/id/S/SU/SUNNAVY/IP-QQWry-0.0.20.tar.gz
    tar zxvf IP-QQWry-0.0.20.tar.gz
    cd IP-QQWry-0.0.20
    perl Makefile.PL     
    make     
    make install

生成log

    less /data/namedx/namedx
    # init syslog
    openlog('namedx', "ndelay,pid", "local6");
    # openlog()：opens a connection to the system logger for a program

    vim /etc/rsyslog.conf
    local6.*                                                /var/log/namedx.log

