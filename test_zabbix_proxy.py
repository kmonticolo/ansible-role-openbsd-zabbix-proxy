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


