# coding: utf-8
import json
import pytest
from check import UyunCheck


def check_ipmi_mock():
    pass


class TestUyunCheck(object):

    @classmethod
    def setup_class(cls):
        cls.base_url = "http://10.1.240.109/"
        cls.apikey = "e10adc3949ba59abbe56e057f2gg88dd"
        cls.alert_id = "2c07d6b7127e47769bd4fcd2f6abcdde"
        cls.res_id = "5ecb29c82350a90cacbbcd71"
        cls.uyun_check = UyunCheck(cls.alert_id, cls.res_id)

    def test_get_alert_number(self):
        """测试获取计算告警的数量"""
        assert self.uyun_check.get_alert_number() == 1

    @pytest.mark.parametrize("cmd, result", [("ping -n 1 10.1.62.106", 0), ("ping -c 1 47.101.131.125", 1)])
    def test_run_cmd(self, cmd, result):
        """测试cmd"""
        get_result = self.uyun_check.run_cmd(cmd)
        assert get_result[0] == result

    @pytest.mark.parametrize("ip, result", [("10.1.100.213", "true"), ("47.101.131.125", "false")])
    def test_ping_ip(self, ip, result):
        assert self.uyun_check.ping_ip(ip) == result

    @pytest.mark.parametrize("ip, port, result", [("10.1.62.106", "22", "true"), ("10.1.62.106", "3306", "false")])
    def test_check_port(self, ip, port, result):
        """测试检查端口"""
        assert self.uyun_check.check_port(ip, port) == result

    @pytest.mark.parametrize("vm_exector_ip, pc_exector_ip, result", [
        ("10.1.100.213", "10.1.62.111",
         (u'10.1.62.106', u'5ec8e1512350a90cacbbcd3b'))
    ])
    def test_get_reource_type(self, vm_exector_ip, pc_exector_ip, result):
        get_result = self.uyun_check.get_reource_type(vm_exector_ip, pc_exector_ip)
        assert get_result == result

    def test_check_ipmi(self):
        """测试检查主机是否上电"""
        get_result = self.uyun_check.check_ipmi()
        pass

    @pytest.mark.parametrize("result_ping, result_ssh, result_impi, result", [
        (json.dumps({"10.1.62.106": "true"}), json.dumps({"10.1.62.106": "true"}), "true", "采控代理异常"),
        (json.dumps({"10.1.62.106": "true"}), json.dumps({"10.1.62.106": "false"}), "true", "主机HANG住"),
        (json.dumps({"10.1.62.106": "false"}), json.dumps({"10.1.62.106": "true"}), "true", "网络不可达"),
        (json.dumps({"10.1.62.106": "false"}), json.dumps({"10.1.62.106": "true"}), "false", "主机宕机"),
    ])
    def test_check_result(self, result_ping, result_ssh, result_impi, result):
        """检查结果"""
        get_result = self.uyun_check.check_result(result_ping, result_ssh, result_impi)
        assert get_result == result

    @pytest.mark.parametrize("result_ping, result_ssh, result_impi, ip", [
        (json.dumps({"10.1.62.106": "true"}), json.dumps({"10.1.62.106": "false"}), "true", "10.1.62.213"),
    ])
    def test_get_result_alert(self, result_ping, result_ssh, result_impi, ip):
        """测试创建一个新的告警"""
        result = self.uyun_check.get_result_alert(result_ping, result_ssh, result_impi, ip)
        assert result == 200
