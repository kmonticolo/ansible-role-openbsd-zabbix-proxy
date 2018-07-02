def test_uname_output(Command):
    command = Command('uname -s')
    assert command.stdout.rstrip() == 'OpenBSD'
    assert command.rc == 0

def test_passwd_file(host):
    passwd = host.file("/etc/passwd")
    assert passwd.contains("root")
    assert passwd.user == "root"
    assert passwd.group == "wheel"
    assert passwd.mode == 0o644

def test_zabbix_user_exists(User):
    '''Check user exists'''
    user = User('_zabbix')
    assert user.exists

def test_zabbix_group_exists(Group):
    '''Check group exists'''
    group = Group('_zabbix')
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

def test_ntpd_service_exists(host):
    service = host.service("ntpd")
    assert service.is_running
    assert service.is_enabled

#zabbix_agentd  zabbix_proxy   

def test_zabbix_agentd_service_exists(host):
    service = host.service("zabbix_agentd")
    assert service.is_running
    assert service.is_enabled

def test_zabbix_proxy_service_exists(host):
    service = host.service("zabbix_proxy")
    assert service.is_running
    assert service.is_enabled

# processes    
def test_zabbix_proxy_process_exists(host):
    process = host.process.filter(user="_zabbix", comm="zabbix_proxy")
    
def test_zabbix_java_process_exists(host):
    process = host.process.get(user="root", comm="java")

def test_command_output(Command):
    command = Command('grep startup.sh /etc/rc.local')
    assert command.stdout.rstrip() == 'PATH=$PATH:/usr/local/jdk-1.8.0/bin/ /usr/local/sbin/zabbix_java/startup.sh'
    assert command.rc == 0

def test_zabbix_proxy_dot_conf(File):
    zabbix_proxy_conf = File("/etc/zabbix/zabbix_proxy.conf")
    assert zabbix_proxy_conf.user == "root"
    assert zabbix_proxy_conf.group == "wheel"
    assert zabbix_proxy_conf.mode == 0o644

    assert zabbix_proxy_conf.contains("ListenPort=10051")
    assert zabbix_proxy_conf.contains("DBHost=localhost")
    assert zabbix_proxy_conf.contains("DebugLevel=3")

def test_port_zabbix_agent_output(Command):
    command = Command('netstat -an|grep ^tcp.*\.10050.*LIST')
    assert command.rc == 0

def test_port_zabbix_proxy_output(Command):
    command = Command('netstat -an|grep ^tcp.*\.10051.*LIST')
    assert command.rc == 0

def test_port_zabbix_java_proxy_output(Command):
    command = Command('netstat -an|grep ^tcp.*\.10052.*LIST')
    assert command.rc == 0

def test_port_mysql_output(Command):
    command = Command('netstat -an|grep ^tcp.*127.0.0.1.3306.*LIST')
    assert command.rc == 0

def test_command_ntpctl_output(Command):
    command = Command('ntpctl -s status | grep "clock synced"')
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
