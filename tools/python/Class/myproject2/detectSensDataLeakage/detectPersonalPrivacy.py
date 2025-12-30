import re
from .StringPatternRecognizer import StringPatternRecognizer

class detectPersonalPrivacy(StringPatternRecognizer):
    def __init__(self) -> None:
        super().__init__() #抽象基类中没有初始化，子类初始化跳过
    
    def find_pattern(self, text: str):
        # self.xxx()调用当前类的xxx()功能，super().xxx()调用父类的xxx()功能
        rule_list = self.get_pattern()
        return super().find_pattern(rule_list)
    
    def get_pattern(self):
        rule_list: dict = {
            "rules": [
                {
                "name": "IDENTITY_CARD",
                "rule": "\\b(\\d{6})(19|20)?(\\d{2})(0[1-9]|1[0-2])(0[1-9]|1\\d|2[0-9]|3[0-1])(\\d{3})(\\d|[Xx])\\b"
            },
            {
                "name": "PASSPORT",
                "rule": "\\b([EeKkGgDdSsPpHh]\\d{8})|((([Ee][a-fA-F])|([DdSsPp][Ee])|([Kk][Jj])|([Mm][Aa])|(1[45]))\\d{7})\\b"
            },
            {
                "name": "CONTACT_MOBILE",
                "rule": "\\b((\\+|00)86)?1((3[\\d])|(4[5,6,7,9])|(5[0-3,5-9])|(6[5-7])|(7[0-8])|(8[\\d])|(9[1,8,9]))\\d{8}\\b"
            },
            {
                "name": "EMAIL_ADDR",
                "rule": "\\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}\\b"
            },
            {
                "name": "BANK_CARD",
                "rule": "\\b([1-9]{1})(\\d{15}|\\d{18})\\b"
            },
            {
                "name": "UNIONPAY_CARD",
                "rule": "\\b[62]\\d{14,17}\\b"
            },
            {
                "name": "VISA_CARD",
                "rule": "\\b4\\d{3}[\\s\\-]?\\d{4}[\\s\\-]?\\d{4}[\\s\\-]?\\d{4}\\b"
            },
            {
                "name": "MASTERCARD_CARD",
                "rule": "\\b(5[1-5]\\d{2})[\\s\\-]?(\\d{4})[\\s\\-]?(\\d{4})[\\s\\-]?(\\d{4})\\b"
            },
            {
                "name": "EXPRESS_CARD",
                "rule": "\\b3[47][0-9]{13}\\b"
            },
            {
                "name": "DISCOVER_CARD",
                "rule": "\\b(6011|622(12[6-9]|1[3-9][0-9]|[2-8][0-9]{2}|9[0-1][0-9]|92[0-5])|64[4-6][0-9]{13})\\b"
            },
            {
                "name": "JCB",
                "rule": "\\b(?:2131|1800|35[0-9]{3})[0-9]{11}\\b"
            },
            {
                "name": "RESIDENCE_PERMIT",
                "rule": "\\b80000(?:19|20)\\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|\\d|3)\\d{3}[\\dX]\\b"
            },
            {
                "name": "HKMP",
                "rule": "\\b[HMhm]{1}([0-9]{10}|[0-9]{8})\\b"
            },
            {
                "name": "TP",
                "rule": "\\b\\d{8}|^[a-zA-Z0-9]{10}|^\\d{18}\\b"
            },
            {
                "name": "SOCIAL_SECURITY_NUMBER",
                "rule": "\\b[\\d]{3}-[\\d]{2}-[\\d]{4}\\b"
            },
            {
                "name": "BIRTHDAY",
                "rule": "\\b(?:(?:\\d{4}[年-]?\\d{2}[月-]?\\d{2}[日]?|\\d{4}-\\d{2}-\\d{2}|\\d{8})|(?:0?[1-9]|1[0-2])[/.\\-](0?[1-9]|[12]\\d|3[01])[/.\\-]\\d{4}|(0?[1-9]|[12]\\d|3[01])[/.\\-](0?[1-9]|1[0-2])[/.\\-]\\d{4})\\b"
            },
            {
                "name": "ADDRESS",
                "rule": "\\b(\\w+省|\\w+自治区)?(\\w+市|\\w+自治州|\\w+地区)?(\\w+区|\\w+县|\\w+市|\\w+镇|\\w+乡|\\w+街道)?(\\w+路|\\w+街|\\w+巷|\\w+村)?(\\d+号|(\\w+号)(\\d+单元)?(\\d+室)?)\\b"
            },
            {
                "name": "APN",
                "rule": "\\b(CMNET|CMWAP|UNIM2M|CTWAP|CTNET|UNINET|3GNET|3GWAP|UNIWAP|3G\\+|UNIWO|CTGPRS|CTLTE|CTM2M)\\b"
            },
            {
                "name": "PLATE_NUMBER",
                "rule": "([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[A-Z]{1}(([0-9]{5}[DF])|([DF]([A-HJ-NP-Z0-9])[0-9]{4})))|([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[A-Z]{1}[A-HJ-NP-Z0-9]{4}[A-HJ-NP-Z0-9挂学警港澳]{1})"
            },
            {
                "name": "ORGANIZATION_CODE",
                "rule": "\\b[0-9A-HJ-NPQRTUWXY]{8}-[0-9A-Z]\\b"
            },
            {
                "name": "SOCIAL_CREDIT_CODE",
                "rule": "\\b([15][1239]|9[123]|Y1)(1[1-5]|2[1-3]|3[1-7]|4[1-6]|5[0-4]|6[1-5])[0-9]{4}[0-9A-Z]{8}[0-9X][0-9A-HJKLMNPQRTUWXY]\\b"
            },
            {
                "name": "BUSINESS_REGISTRATION_CODE",
                "rule": "\\b((1[1-5]|2[1-3]|3[1-7]|4[1-6]|5[0-4]|6[1-5])[0-9]{4}|100000)[0-5][1-5][0-2][0-9]{6}\\b"
            },
            {
                "name": "GPS_DECIMAL ",
                "rule": "\\b-?([1-9]\\d|\\d)(.\\d+)?, ?-?([1-9]\\d|\\d)(.\\d+)?\\b"
            },
            {
                "name": "GPS_DEGREES",
                "rule": "\\b-?([1-9]\\d|\\d)°([1-5]?\\d)'([1-5]?\\d.?\\d*)\"[WE], ?-?([1-9]\\d|\\d)°([1-5]?\\d)'([1-5]?\\d.?\\d*)\"[NS]\\b"
            },
            {
                "name": "UTM",
                "rule": "\\b\\d{1,2}[CDEFGHJKLMNPQRSTUVWX][A-Za-z]{2} \\d{1,7} \\d{1,7}\\b"
            },
            {
                "name": "MAC",
                "rule": "\\b([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\\b"
            },
            {
                "name": "IPV4",
                "rule": "\\b(\\d{1,2}|1\\d\\d|2[0-4]\\d|25[0-5])\\.(\\d{1,2}|1\\d\\d|2[0-4]\\d|25[0-5])\\.(\\d{1,2}|1\\d\\d|2[0-4]\\d|25[0-5])\\.(\\d{1,2}|1\\d\\d|2[0-4]\\d|25[0-5])\\b"
            },
            {
                "name": "IPV6",
                "rule": "\\b([\\da-fA-F]{1,4}:){6}((25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.){3}(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)$|^::([\\da-fA-F]{1,4}:){0,4}((25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.){3}(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)$|^([\\da-fA-F]{1,4}:):([\\da-fA-F]{1,4}:){0,3}((25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.){3}(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)$|^([\\da-fA-F]{1,4}:){2}:([\\da-fA-F]{1,4}:){0,2}((25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.){3}(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)$|^([\\da-fA-F]{1,4}:){3}:([\\da-fA-F]{1,4}:){0,1}((25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.){3}(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)$|^([\\da-fA-F]{1,4}:){4}:((25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.){3}(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)$|^([\\da-fA-F]{1,4}:){7}[\\da-fA-F]{1,4}$|^:((:[\\da-fA-F]{1,4}){1,6}|:)$|^[\\da-fA-F]{1,4}:((:[\\da-fA-F]{1,4}){1,5}|:)$|^([\\da-fA-F]{1,4}:){2}((:[\\da-fA-F]{1,4}){1,4}|:)$|^([\\da-fA-F]{1,4}:){3}((:[\\da-fA-F]{1,4}){1,3}|:)$|^([\\da-fA-F]{1,4}:){4}((:[\\da-fA-F]{1,4}){1,2}|:)$|^([\\da-fA-F]{1,4}:){5}:([\\da-fA-F]{1,4})?$|^([\\da-fA-F]{1,4}:){6}:\\b"
            },
            {
                "name": "NET_MASK",
                "rule": "\\b(254|252|248|240|224|192|128)\\.0\\.0\\.0|255\\.(254|252|248|240|224|192|128|0)\\.0\\.0|255\\.255\\.(254|252|248|240|224|192|128|0)\\.0|255\\.255\\.255\\.(254|252|248|240|224|192|128|0)\\b"
            },
            {
                "name": "BASE_STATION_ID",
                "rule": "\\b(\\d{5,6})-(\\d{2,3})-(\\d{2,3})\\b"
            },
            {
                "name": "IMSI",
                "rule": "\\b4600[0,1,2,3,5,6,7]\\d{10}\\b"
            },
            {
                "name": "NETWORK_SEGMENT",
                "rule": "\\b((\\d{1,2}|1\\d\\d|2[0-4]\\d|25[0-5])\\.(\\d{1,2}|1\\d\\d|2[0-4]\\d|25[0-5])\\.(\\d{1,2}|1\\d\\d|2[0-4]\\d|25[0-5])\\.(\\*))\\b"
            },
            {
                "name": "WEBSITE",
                "rule": "\\b(https?|ftp)://[^\\s/$.?#].[^\\s]*\\b"
            }
            ]
        }

        return rule_list
    
    def _compile_reg(self, rules: dict):
        compiled_reg_list = []
        for rule in rules["rules"]:
            name = rule["name"]
            reg_ex = rule["rule"]
            compiled_reg = {
                "name": name, 
                "compiled_rule": re.compile(reg_ex)
            }
            compiled_reg_list.append(compiled_reg)

        return compiled_reg_list

    def describe(self):
        return super().describe()