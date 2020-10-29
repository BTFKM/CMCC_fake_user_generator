# coding=utf-8
import random
import numpy as np
import uuid
import csv


class Contract:
    def __init__(self):
        self.contract_id = None
        self.create_contract()

    def create_contract(self):
        self.contract_id = 'CONID' + str(''.join(random.sample('123456789', 4)))


class ContractList:
    def __init__(self, contract_num=20):
        self.contract_num = contract_num
        self.contract_list = []
        self.create_contract_list()

    def create_contract_list(self):
        for _ in range(self.contract_num):
            self.contract_list.append(Contract())


class Chn:
    def __init__(self):
        self.chn_id = None
        self.chn_type = None
        self.chn_type_list = ['A-type', 'B-type', 'C-type', 'D-type']
        self.create_chn()

    def create_chn(self):
        self.chn_id = 'CHN' + str(''.join(random.sample('123456789', 4)))
        self.chn_type = self.chn_type_list[random.randint(0, len(self.chn_type_list) - 1)]


class Depart:
    def __init__(self):
        self.depart_id = 'DEP' + str(''.join(random.sample('123456789', 4)))


class ChnAndDepartList:
    def __init__(self, chn_num=50, dep_num=10):
        self.chn_num = chn_num
        self.dep_num = dep_num
        self.dep_chn_relation = {}
        self.create_relation()

    def create_relation(self):
        for i in range(self.dep_num):
            new_dep = Depart()
            self.dep_chn_relation[new_dep.depart_id] = []
            for j in range(int(self.chn_num / self.dep_num) * i, int(self.chn_num / self.dep_num) * (i + 1)):
                new_chn = Chn()
                self.dep_chn_relation[new_dep.depart_id].append([new_chn.chn_id, new_chn.chn_type])
                # {'depart_id': [chn_id, chn_type]}


class Dinner:
    def __init__(self):
        self.dinner_id = ''  # 产品id
        self.discharge_in_dinner = None  # 套内流量
        self.call_in_dinner = None  # 套内语音
        self.sms_in_dinner = None  # 套内短信
        self.avg_arpu = None  # 套餐平均arpu
        self.if_5g = None  # 5G套餐
        self.dinner_net_type = None
        self.avg_arpu_list = [5, 10, 20, 30, 50, 55, 60, 65, 70, 75, 80, 100, 150, 200]
        self.create_dinner()

    def create_dinner(self):
        for _ in range(0, 8):
            self.dinner_id += str(random.randint(0, 10))
        self.dinner_id = 'DIN' + self.dinner_id
        random_no = random.randint(0, len(self.avg_arpu_list) - 1)
        self.avg_arpu = self.avg_arpu_list[random_no] + random.randint(-10, 10)
        if self.avg_arpu < 5: self.avg_arpu = 5
        discharge_random = random.uniform(0.3, 0.4)
        print(discharge_random)
        self.if_5g = True if discharge_random >= 0.37 else False
        self.discharge_in_dinner = int((self.avg_arpu * discharge_random * 800) * (1 + 0.2 * self.if_5g) / 100) * 100
        self.call_in_dinner = int((self.avg_arpu * random.uniform(0.5, 0.7) * 60) * (1 + 0.2 * self.if_5g) / 100) * 100
        self.sms_in_dinner = int((self.avg_arpu * random.uniform(0.05, 0.1) * 10))
        self.dinner_net_type = 4 if not self.if_5g else 5


class Device:
    def __init__(self):
        self.if_smart_phone = None  # 是否智能终端
        self.device_type = None  # 终端机型
        self.device_producer = None  # 终端厂家
        self.if_device_support_5G = None  # 终端是否支持5G
        self.create_device()

    def create_device(self):
        self.device_producer = 'DPR' + str(''.join(random.sample('zyxwvutsrqponmlkjihgfedcba'.upper(), 5)))
        if random.randint(0, 21) > 5:
            self.if_smart_phone = True
            if random.randint(0, 20) > 10:
                self.if_device_support_5G = True
            else:
                self.if_device_support_5G = False
        else:
            self.if_smart_phone = False
            self.if_device_support_5G = False
        self.device_type = 'DTY' + str(''.join(random.sample('123456789', 8)))


class DinnerList:
    def __init__(self, dinner_number=100):
        self.dinner_num = dinner_number
        self.dinner_list = []
        self.dinner_generator()

    def dinner_generator(self):
        for i in range(self.dinner_num):
            self.dinner_list.append(Dinner())

    def get_dinner_list(self):
        return self.dinner_list

    def get_one_dinner(self):
        return self.dinner_list[random.randint(0, len(self.dinner_list) - 1)]


def user_use_state(dinner: Dinner, device: Device):
    speed = [20, 300, 500, 1000]
    avg_arpu = dinner.avg_arpu
    discharge_in_dinner = dinner.discharge_in_dinner  # 套内流量
    call_in_dinner = dinner.call_in_dinner  # 套内语音
    sms_in_dinner = dinner.sms_in_dinner  # 套内短信
    avg_arpu = dinner.avg_arpu  # 套餐平均arpu
    if_5g = dinner.if_5g  # 5G套餐
    dinner_net_type = dinner.dinner_net_type

    if_smart_phone = device.if_smart_phone  # 是否智能终端
    device_type = device.device_type  # 终端机型
    device_producer = device.device_producer  # 终端厂家
    if_device_support_5g = device.if_device_support_5G  # 终端是否支持5G

    # discharge dischargeextra call  msm  arpu discharge_extra_fee_1

    boost = (random.uniform(1, 1.1) if if_smart_phone else random.uniform(0.2, 0.5)) * (
        random.uniform(1.5, 3) if if_device_support_5g else random.uniform(0.8, 1.2))

    discharge = int(
        avg_arpu * 30 * random.uniform(0.8, 1.5) * boost) + dinner.discharge_in_dinner * random.uniform(
        0.5, 0.8)
    dischargeextra = discharge - discharge_in_dinner
    if dischargeextra <= 0: dischargeextra = 0
    call = int(call_in_dinner * random.uniform(0.5, 1.2) * boost)
    sms = int(sms_in_dinner * random.uniform(-0.3, 0.2))
    if sms < 0: sms = 0
    arpu = int(avg_arpu + dischargeextra * (1 / 500) + random.randint(5, 30) * boost)
    discharge_extra_fee = int(dischargeextra * (1 / 500))

    return discharge, dischargeextra, discharge_extra_fee, call, sms, arpu


class DeviceList:
    def __init__(self, device_num=30):
        self.device_num = device_num
        self.device_list = []
        self.device_generator()

    def device_generator(self):
        for i in range(self.device_num):
            self.device_list.append(Device())

    def get_device_list(self):
        return self.device_list

    def get_one_device(self):
        return self.device_list[random.randint(0, len(self.device_list) - 1)]


def get_one_5g_device(device_list: DeviceList):
    device_5g = []
    for i in range(len(device_list.device_list)):
        if device_list.device_list[i].if_device_support_5G:
            device_5g.append(device_list.device_list[i])
    return device_5g[random.randint(0, len(device_5g) - 1)]


class User:
    def __init__(self, dinner_list: DinnerList, device_list: DeviceList, chn_dep_dict: ChnAndDepartList,
                 contract_list: ContractList):
        self.dinner_list = dinner_list
        self.device_list = device_list
        self.chn_dep_dict = chn_dep_dict
        self.contract_list = contract_list
        # self.no = None  # 序号标识
        self.service_id = None  # 用户id
        self.in_date = None  # 入网时间
        self.contract_chn_id = None  # 合约办理渠道
        self.contract_chn_type = None  # 合约办理渠道类型
        self.contract_depart_id = None  # 合约基层单元
        self.contract_id = None  # 合约id
        self.if_contract = None  # 是否合约
        self.dinner_id = None  # 产品id
        # self.dinner_id_before_contract = None  # 合约前套餐id
        # self.active_level_before_contract = None  # 合约前活动档位
        # self.dinner_id_after_contract = None  # 合约后套餐id
        # self.active_level_after_contract = None  # 合约后活动档位
        self.if_dinner_grow = None  # 是否升套
        self.if_arpu_grow = None  # 增降收预判
        self.arpu_1 = None  # T-2月 出账收入
        self.arpu_2 = None  # t-1 出账收入
        self.arpu_3 = None  # t 出账收入
        self.discharge_1 = None  # T-2月 流量
        self.discharge_2 = None  # t-1 流量
        self.discharge_3 = None  # t 流量
        self.discharge_extra_1 = None  # T-2月 套外流量
        self.discharge_extra_2 = None  # t-1 套外流量
        self.discharge_extra_3 = None  # t 套外流量
        self.discharge_extra_fee_1 = None  # T-2月 套外流量费用
        self.discharge_extra_fee_2 = None  # t-1 套外流量费用
        self.discharge_extra_fee_3 = None  # t 套外流量费用
        self.call_1 = None  # T-2月 通话
        self.call_2 = None  # t-1 通话
        self.call_3 = None  # t 通话
        self.msm_1 = None  # T-2月 发出短信
        self.msm_2 = None  # t-1 发出短信
        self.msm_3 = None  # t 发出短信
        self.if_change_dinner = None  # 是否改套
        self.if_dx = None  # 是否低消
        self.if_5g = None  # 是否5G
        self.if_wk_upgrade = None  # 是否王卡升级
        self.in_net_age = None  # 用户网龄(月)
        self.dinner_net_type = None  # 用户基本套餐类型 2 3 4 5G
        self.birthday = None  # 生日
        self.user_level = None  # 用户星级
        self.discharge_in_dinner = None  # 套内流量
        self.call_in_dinner = None  # 套内语音
        self.sms_in_dinner = None  # 套内短信
        self.if_zhwj = None  # 是否智慧沃家
        self.if_smart_phone = None  # 是否智能终端
        self.device_type = None  # 终端机型
        self.device_producer = None  # 终端厂家
        self.if_device_support_5G = None  # 终端是否支持5G
        self.if_5G_station_near_by = None  # 附近是否5G基站
        self.avg_arpu = None
        self.create_user()

    def create_user(self):
        import datetime
        from dateutil.relativedelta import relativedelta
        date_now = datetime.datetime.now()
        user_device = self.device_list.device_list[random.randint(0, len(self.device_list.device_list) - 1)]
        user_dinner = self.dinner_list.dinner_list[random.randint(0, len(self.dinner_list.dinner_list) - 1)]

        self.service_id = str(uuid.uuid4())

        in_month_diff = random.randint(1, 4 * 24)
        birth_month_deff = in_month_diff + random.randint(1, 30 * 24)
        self.in_net_age = in_month_diff
        self.in_date = datetime.datetime.strftime(date_now - relativedelta(months=in_month_diff), '%Y%m')
        self.birthday = datetime.datetime.strftime(
            date_now - relativedelta(months=in_month_diff) - relativedelta(months=birth_month_deff), '%Y%m')
        self.contract_depart_id = list(self.chn_dep_dict.dep_chn_relation.keys())[
            random.randint(0, len(list(self.chn_dep_dict.dep_chn_relation.keys())) - 1)]

        self.contract_chn_id = self.chn_dep_dict.dep_chn_relation[self.contract_depart_id][
            random.randint(0, len(self.chn_dep_dict.dep_chn_relation[self.contract_depart_id]) - 1)][0]
        self.contract_chn_type = self.chn_dep_dict.dep_chn_relation[self.contract_depart_id][
            random.randint(0, len(self.chn_dep_dict.dep_chn_relation[self.contract_depart_id]) - 1)][1]
        self.if_contract = True if random.random() > 0.7 else False
        if self.if_contract:
            # print(len(self.contract_list.contract_list))
            self.contract_id = self.contract_list.contract_list[
                random.randint(0, len(self.contract_list.contract_list) - 1)].contract_id

        dinner = dinner_list.get_one_dinner()
        self.dinner_id = dinner.dinner_id
        self.discharge_in_dinner = dinner.discharge_in_dinner  # 套内流量
        self.call_in_dinner = dinner.call_in_dinner  # 套内语音
        self.sms_in_dinner = dinner.sms_in_dinner  # 套内短信
        self.dinner_net_type = dinner.dinner_net_type

        device = device_list.get_one_device()
        self.if_smart_phone = device.if_smart_phone  # 是否智能终端
        self.device_type = device.device_type  # 终端机型
        self.device_producer = device.device_producer  # 终端厂家
        self.if_device_support_5G = device.if_device_support_5G  # 终端是否支持5G
        # discharge, dischargeextra, discharge_extra_fee, call, sms, arpu
        self.discharge_1, self.discharge_extra_1, self.discharge_extra_fee_1, self.call_1, self.msm_1, self.arpu_1 = user_use_state(
            dinner, device)
        self.discharge_2, self.discharge_extra_2, self.discharge_extra_fee_2, self.call_2, self.msm_2, self.arpu_2 = user_use_state(
            dinner, device)
        self.discharge_3, self.discharge_extra_3, self.discharge_extra_fee_3, self.call_3, self.msm_3, self.arpu_3 = user_use_state(
            dinner, device)

        self.if_zhwj = True if random.uniform(0, 1) > 0.8 else False
        self.if_5G_station_near_by = True if random.uniform(0, 1) > 0.4 else False
        self.if_dx = True if random.uniform(0, 1) > 0.9 else False
        self.user_level = random.choice([1, 2, 3, 3, 3, 4, 4, 5])

        self.avg_arpu = dinner.avg_arpu

    def get_user(self):
        return {
            'service_id': self.service_id,
            'in_date': self.in_date,
            'contract_chn_id': self.contract_chn_id,
            'contract_chn_type': self.contract_chn_type,
            'contract_depart_id': self.contract_depart_id,
            'contract_id': self.contract_id,
            'if_contract': self.if_contract,
            'dinner_id': self.dinner_id,
            'if_dinner_grow': self.if_dinner_grow,
            'if_arpu_grow': self.if_arpu_grow,
            'arpu_1': round(self.arpu_1),
            'arpu_2': round(self.arpu_2),
            'arpu_3': round(self.arpu_3),
            'discharge_1': round(self.discharge_1),
            'discharge_2': round(self.discharge_2),
            'discharge_3': round(self.discharge_3),
            'discharge_extra_1': round(self.discharge_extra_1),
            'discharge_extra_2': round(self.discharge_extra_2),
            'discharge_extra_3': round(self.discharge_extra_3),
            'discharge_extra_fee_1': round(self.discharge_extra_fee_1),
            'discharge_extra_fee_2': round(self.discharge_extra_fee_2),
            'discharge_extra_fee_3': round(self.discharge_extra_fee_3),
            'call_1': round(self.call_1),
            'call_2': round(self.call_2),
            'call_3': round(self.call_3),
            'msm_1': round(self.msm_1),
            'msm_2': round(self.msm_2),
            'msm_3': round(self.msm_3),
            'if_change_dinner': self.if_change_dinner,
            'if_dx': self.if_dx,
            # 'if_5g': self.if_5g,
            'if_wk_upgrade': self.if_wk_upgrade,
            'in_net_age': self.in_net_age,
            'dinner_net_type': self.dinner_net_type,
            'birthday': self.birthday,
            'user_level': self.user_level,
            'discharge_in_dinner': self.discharge_in_dinner,
            'call_in_dinner': self.call_in_dinner,
            'sms_in_dinner': self.sms_in_dinner,
            'if_zhwj': self.if_zhwj,
            'if_smart_phone': self.if_smart_phone,
            'device_type': self.device_type,
            'device_producer': self.device_producer,
            'if_device_support_5G': self.if_device_support_5G,
            'if_5G_station_near_by': self.if_5G_station_near_by,
            'avg_arpu': self.avg_arpu
        }


def feature_5g(user: User, device_list: DeviceList):
    discharge_modify = np.array([random.uniform(1.4, 1.9)] * 3)
    call_modify = np.array([random.uniform(0.9, 1.1)] * 3)
    sms_modify = np.array([random.uniform(0.9, 1.1)] * 3)
    arpu_modify = np.array([random.uniform(0.9, 1.2)] * 3)
    user.discharge_1, user.discharge_2, user.discharge_3 = np.array(
        [user.discharge_1, user.discharge_2, user.discharge_3]) * discharge_modify
    user.call_1, user.call_2, user.call_3 = np.array([user.call_1, user.call_2, user.call_3]) * call_modify
    user.msm_1, user.msm_2, user.msm_3 = np.array([user.msm_1, user.msm_2, user.msm_3]) * sms_modify
    user.arpu_1, user.arpu_2, user.arpu_3 = np.array([user.arpu_1, user.arpu_2, user.arpu_3]) * arpu_modify

    discharge_extra_1_old, discharge_extra_2_old, discharge_extra_3_old = user.discharge_extra_1, user.discharge_extra_2, user.discharge_extra_3

    user.discharge_extra_1, user.discharge_extra_2, user.discharge_extra_3 = np.array(
        [user.discharge_1, user.discharge_2, user.discharge_3]) - np.array(
        [user.discharge_in_dinner] * 3)
    if user.discharge_extra_1 < 0:  user.discharge_extra_1 = 0
    if user.discharge_extra_2 < 0:  user.discharge_extra_2 = 0
    if user.discharge_extra_3 < 0:  user.discharge_extra_3 = 0
    user.discharge_extra_fee_1, user.discharge_extra_fee_2, user.discharge_extra_fee_3 = np.array(
        [user.discharge_extra_1, user.discharge_extra_2, user.discharge_extra_3]) * np.array(
        [1 / 500] * 3)
    user.arpu_1 += user.discharge_extra_fee_1  # - (user.discharge_extra_1 - discharge_extra_1_old) * (1 / 1000)
    user.arpu_2 += user.discharge_extra_fee_2  # - (user.discharge_extra_2 - discharge_extra_2_old) * (1 / 1000)
    user.arpu_3 += user.discharge_extra_fee_3  # - (user.discharge_extra_3 - discharge_extra_3_old) * (1 / 1000)
    user.if_dinner_grow = True if random.uniform(0, 1) > 0.3 else False
    user.if_arpu_grow = True if random.uniform(0, 1) > 0.3 else False
    user.if_zhwj = True if random.uniform(0, 1) > 0.3 else False
    user.if_5G_station_near_by = True if random.uniform(0, 1) > 0.3 else False

    user.if_smart_phone = True
    if_modfiy_5g_device = True if random.uniform(0, 1) > 0 else False
    if if_modfiy_5g_device:
        new_device = get_one_5g_device(device_list)
        user.device_type, user.device_producer, user.if_device_support_5G = new_device.device_type, new_device.device_producer, new_device.if_device_support_5G
    return user


if __name__ == '__main__':
    dinner_list = DinnerList(dinner_number=50)
    device_list = DeviceList()
    chn_dep_dict = ChnAndDepartList()
    contract_list = ContractList()
    user_list = []
    user_limit = 40000
    for _ in range(user_limit):
        user_list.append(User(dinner_list=dinner_list, device_list=device_list, chn_dep_dict=chn_dep_dict,
                              contract_list=contract_list))

    user_5g_list = []
    num = 0

    user_to_5g_limit = int(user_limit * (1 / 500))
    for _ in range(user_limit):
        if num >= user_to_5g_limit:
            break
        if user_list[_].dinner_net_type != 4:
            user_list[_] = feature_5g(user_list[_], device_list)
            num += 1

    headers = ['service_id',
               'in_date',
               'contract_chn_id',
               'contract_chn_type',
               'contract_depart_id',
               'contract_id',
               'if_contract',
               'dinner_id',
               'if_dinner_grow',
               'if_arpu_grow',
               'arpu_1',
               'arpu_2',
               'arpu_3',
               'discharge_1',
               'discharge_2',
               'discharge_3',
               'discharge_extra_1',
               'discharge_extra_2',
               'discharge_extra_3',
               'discharge_extra_fee_1',
               'discharge_extra_fee_2',
               'discharge_extra_fee_3',
               'call_1',
               'call_2',
               'call_3',
               'msm_1',
               'msm_2',
               'msm_3',
               'if_change_dinner',
               'if_dx',
               'if_5g',
               'if_wk_upgrade',
               'in_net_age',
               'dinner_net_type',
               'birthday',
               'user_level',
               'discharge_in_dinner',
               'call_in_dinner',
               'sms_in_dinner',
               'if_zhwj',
               'if_smart_phone',
               'device_type',
               'device_producer',
               'if_device_support_5G',
               'if_5G_station_near_by',
               'avg_arpu'
               ]
    csv_list = []
    for i in range(len(user_list)):
        row_temp = [user_list[i].service_id,
                    user_list[i].in_date,
                    user_list[i].contract_chn_id,
                    user_list[i].contract_chn_type,
                    user_list[i].contract_depart_id,
                    user_list[i].contract_id,
                    user_list[i].if_contract,
                    user_list[i].dinner_id,
                    user_list[i].if_dinner_grow,
                    user_list[i].if_arpu_grow,
                    user_list[i].arpu_1,
                    user_list[i].arpu_2,
                    user_list[i].arpu_3,
                    user_list[i].discharge_1,
                    user_list[i].discharge_2,
                    user_list[i].discharge_3,
                    user_list[i].discharge_extra_1,
                    user_list[i].discharge_extra_2,
                    user_list[i].discharge_extra_3,
                    user_list[i].discharge_extra_fee_1,
                    user_list[i].discharge_extra_fee_2,
                    user_list[i].discharge_extra_fee_3,
                    user_list[i].call_1,
                    user_list[i].call_2,
                    user_list[i].call_3,
                    user_list[i].msm_1,
                    user_list[i].msm_2,
                    user_list[i].msm_3,
                    user_list[i].if_change_dinner,
                    user_list[i].if_dx,
                    user_list[i].if_5g,
                    user_list[i].if_wk_upgrade,
                    user_list[i].in_net_age,
                    user_list[i].dinner_net_type,
                    user_list[i].birthday,
                    user_list[i].user_level,
                    user_list[i].discharge_in_dinner,
                    user_list[i].call_in_dinner,
                    user_list[i].sms_in_dinner,
                    user_list[i].if_zhwj,
                    user_list[i].if_smart_phone,
                    user_list[i].device_type,
                    user_list[i].device_producer,
                    user_list[i].if_device_support_5G,
                    user_list[i].if_5G_station_near_by,
                    user_list[i].avg_arpu]
        csv_list.append(row_temp)
    with open('user.csv', 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(csv_list)

    headers = ['dinner_id', 'discharge_in_dinner', 'call_in_dinner', 'sms_in_dinner', 'avg_arpu', 'dinner_net_type']
    csv_list = []
    for i in range(len(dinner_list.dinner_list)):
        row_temp = [dinner_list.dinner_list[i].dinner_id, dinner_list.dinner_list[i].discharge_in_dinner,
                    dinner_list.dinner_list[i].call_in_dinner, dinner_list.dinner_list[i].sms_in_dinner,
                    dinner_list.dinner_list[i].avg_arpu, dinner_list.dinner_list[i].dinner_net_type]
        csv_list.append(row_temp)
    with open('product.csv', 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(csv_list)
