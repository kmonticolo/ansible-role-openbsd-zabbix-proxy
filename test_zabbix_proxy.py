def test_uname_output(host):
    command = host.command('uname -s')
    assert command.stdout.rstrip() == 'OpenBSD'
    assert command.rc == 0

def test_passwd_file(host):
    passwd = host.file("/etc/passwd")
    assert passwd.contains("root")
    assert passwd.user == "root"
    assert passwd.group == "wheel"
    assert passwd.mode == 0o644

def test_zabbix_user_exists(host):
    '''Check user exists'''
    user = host.user('_zabbix')
    assert user.exists
    assert user.name == "_zabbix"
    assert user.group == "_zabbix"
    assert user.shell == "/sbin/nologin"
    assert user.home == "/nonexistent"

def test_zabbix_group_exists(host):
    '''Check group exists'''
    group = host.group('_zabbix')
    assert group.exists

def test_zabbix_proxy_file(host):
    binary = host.file("/usr/local/sbin/zabbix_proxy")
    assert binary.user == "root"
    assert binary.group == "wheel"
    assert binary.mode == 0o755

def test_java_settings_file(host):
    file = host.file("/usr/local/sbin/zabbix_java/settings.sh")
    assert file.user == "root"
    assert file.group == "wheel"
    assert file.mode == 0o644
    assert file.contains("^START_POLLERS=20")
    assert file.contains("^PID_FILE=\"/var/run/zabbix/zabbix_java.pid\"")

def test_java_shutdown_file(host):
    file = host.file("/usr/local/sbin/zabbix_java/shutdown.sh")
    assert file.user == "root"
    assert file.group == "wheel"
    assert file.mode == 0o755

def test_java_startup_file(host):
    file = host.file("/usr/local/sbin/zabbix_java/startup.sh")
    assert file.user == "root"
    assert file.group == "wheel"
    assert file.mode == 0o755

def test_zabbix_agent_package_exists(host):
    package = host.package("zabbix-agent")
    assert package.is_installed

def test_arping_package_exists(host):
    package = host.package("arping")
    assert package.is_installed

def test_fping_package_exists(host):
    package = host.package("fping")
    assert package.is_installed

def test_jdk_package_exists(host):
    package = host.package("jdk")
    assert package.is_installed

def test_mariadbclient_package_exists(host):
    package = host.package("mariadb-client")
    assert package.is_installed

def test_mariadbserver_package_exists(host):
    package = host.package("mariadb-server")
    assert package.is_installed

def test_nmap_package_exists(host):
    package = host.package("nmap")
    assert package.is_installed

# services

def test_mysql_service_exists(host):
    service = host.service("mysqld")
    assert service.is_running
    assert service.is_enabled
    mysql = host.process.get(comm="mysqld")
    assert mysql.user == "_mysql"
    assert mysql.group == "_mysql"

def test_ntpd_service_exists(host):
    service = host.service("ntpd")
    assert service.is_running
    assert service.is_enabled

#zabbix_agentd  zabbix_proxy   

def test_zabbix_agentd_service_exists(host):
    service = host.service("zabbix_agentd")
    assert service.is_running
    assert service.is_enabled
    process = host.process.filter(user="_zabbix", group="_zabbix", comm="zabbix_agentd")

def test_zabbix_proxy_service_exists(host):
    service = host.service("zabbix_proxy")
    assert service.is_running
    assert service.is_enabled
    process = host.process.filter(comm="zabbix_proxy")

# processes    
def test_zabbix_proxy_process_exists(host):
    process = host.process.filter(user="_zabbix", group="_zabbix", comm="zabbix_proxy")
    
def test_zabbix_java_process_exists(host):
    process = host.process.get(user="root", comm="java")

def test_command_output(host):
    command = host.command('grep startup.sh /etc/rc.local')
    assert command.stdout.rstrip() == 'PATH=$PATH:/usr/local/jdk-1.8.0/bin/ /usr/local/sbin/zabbix_java/startup.sh'
    assert command.rc == 0

def test_zabbix_proxy_dot_conf(host):
    zabbix_proxy_conf = host.file("/etc/zabbix/zabbix_proxy.conf")
    assert zabbix_proxy_conf.user == "root"
    assert zabbix_proxy_conf.group == "wheel"
    assert zabbix_proxy_conf.mode == 0o644
    assert zabbix_proxy_conf.contains("^DBHost=localhost")
    assert zabbix_proxy_conf.contains("^Server=172.31.253.146")
    assert zabbix_proxy_conf.contains("^Hostname=Zabbix proxy")
    assert zabbix_proxy_conf.contains("^LogFile=/var/zabbix/zabbix_proxy.log")
    assert zabbix_proxy_conf.contains("^EnableRemoteCommands=1")
    assert zabbix_proxy_conf.contains("^DBHost=localhost")
    assert zabbix_proxy_conf.contains("^DBName=zabbix_proxy")
    assert zabbix_proxy_conf.contains("^DBUser=zabbix")
    assert zabbix_proxy_conf.contains("^DBPassword=zabbix")
    assert zabbix_proxy_conf.contains("^ConfigFrequency=300")
    assert zabbix_proxy_conf.contains("^StartPollers=35")
    assert zabbix_proxy_conf.contains("^StartPollersUnreachable=5")
    assert zabbix_proxy_conf.contains("^StartPingers=5")
    assert zabbix_proxy_conf.contains("^StartDiscoverers=5")
    assert zabbix_proxy_conf.contains("^StartHTTPPollers=10")
    assert zabbix_proxy_conf.contains("^JavaGateway=172.16.160.24")
    assert zabbix_proxy_conf.contains("^JavaGatewayPort=10052")
    assert zabbix_proxy_conf.contains("^StartJavaPollers=20")
    assert zabbix_proxy_conf.contains("^CacheSize=12M")
    assert zabbix_proxy_conf.contains("^HistoryCacheSize=8M")
    assert zabbix_proxy_conf.contains("^HistoryIndexCacheSize=4M")
    assert zabbix_proxy_conf.contains("^Timeout=5")
    assert zabbix_proxy_conf.contains("^UnreachableDelay=5")
    assert zabbix_proxy_conf.contains("^FpingLocation=/usr/local/sbin/fping")
    assert zabbix_proxy_conf.contains("^LogSlowQueries=3000")
    assert zabbix_proxy_conf.contains("^User=_zabbix")

def test_port_zabbix_agent_output(host):
    command = host.command('netstat -an|grep ^tcp.*\.10050.*LIST')
    assert command.rc == 0

def test_port_zabbix_proxy_output(host):
    command = host.command('netstat -an|grep ^tcp.*\.10051.*LIST')
    assert command.rc == 0

def test_port_zabbix_java_proxy_output(host):
    command = host.command('netstat -an|grep ^tcp.*\.10052.*LIST')
    assert command.rc == 0

def test_port_mysql_output(host):
    command = host.command('netstat -an|grep ^tcp.*127.0.0.1.3306.*LIST')
    assert command.rc == 0

def test_command_ntpctl_output(host):
    command = host.command('ntpctl -s status | grep "clock synced"')
    assert command.rc == 0

#sysctl
def test_sysctl_semni(host):
    sysctl = host.sysctl("kern.seminfo.semmni")
    assert sysctl == 120

def test_sysctl_semns(host):
    sysctl = host.sysctl("kern.seminfo.semmns")
    assert sysctl == 300

def test_sysctl_semnu(host):
    sysctl = host.sysctl("kern.seminfo.semmnu")
    assert sysctl == 600

def test_sysctl_semopm(host):
    sysctl = host.sysctl("kern.seminfo.semopm")
    assert sysctl == 300

def test_sysctl_semmsl(host):
    sysctl = host.sysctl("kern.seminfo.semmsl")
    assert sysctl == 240

def test_sysctl_file(host):
    file = host.file("/etc/sysctl.conf")
    assert file.contains("kern.seminfo.semmni=120")
    assert file.contains("kern.seminfo.semmns=300")
    assert file.contains("kern.seminfo.semmnu=600")
    assert file.contains("kern.seminfo.semopm=300")
    assert file.contains("kern.seminfo.semmsl=240")
