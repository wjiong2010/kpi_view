import os
import csv

report_head = '''任务量等级： 5:非常饱满， 4:饱满，3：适中，2：不足，1：严重不足'''
report_main_seperator = '''================================================================================='''
report_secondary_seperator = '''------------------------------------------------------------------------'''
report_summary = '''总结：'''


class KPIItem:
    def __init__(self):
        self.name_list = []
        self.status_counter = {}
        self.total = 0

    def reset(self):
        # self.name_list.clear()
        self.total = 0
        keys_list = list(self.status_counter.keys())
        for k in keys_list:
            self.status_counter[k] = 0

    def get_info(self):
        # line_format = "{0:>40},{1:>40}"
        ts = " " * 4
        for s in self.name_list:
            ts += s
            ts += '&'
        ts = ts.strip('&')
        ts += ', total {0}:\n'.format(self.total)

        keys_list = list(self.status_counter.keys())
        for k in keys_list:
            if self.status_counter[k] != 0:
                ts += " " * 8 + k + ': ' + str(self.status_counter[k]) + '\n'
        # print(ts)
        return ts

    def do_proc(self, id_v, st, ty):
        print(f"ID: {id_v}, Status: {st}, Type: {ty} in {self.name_list}")
        i = st.find('（')
        st = st[:i]
        self.total += 1
        keys_list = list(self.status_counter.keys())
        for k in keys_list:
            print(f"checking {st} in {k}")
            if -1 != k.find(st):
                print(f"{st} in {k}")
                self.status_counter[k] += 1
                break

    def summary(self, rt_list, pre):
        d = self.status_counter
        c = 0
        for r in rt_list:
            c += d[r]
        # ratio = d["NO_FEEDBACK"] + d["RESOLVED"] + d["REJECTED"] + d["WAIT_RELEASE"] + d["CLOSED-关闭"]
        ratio = "{:.1f}".format(float(c / self.total) * 100.0)

        # self.summary = "FAE_BUG fixed: " + str(ratio) + "%"
        return " " * 4 + pre + str(ratio) + "%"


class itemFAEBUG(KPIItem):
    def __init__(self):
        super().__init__()
        self.name_list = ["FAE_BUG"]
        self.status_counter = {
            "NO_FEEDBACK": 0,
            "RESOLVED": 0,
            "WAIT_FEEDBACK": 0,
            "NEW": 0,
            "DOING": 0,
            "ASSIGNED": 0,
            "PENDING": 0,
            "TESTING": 0,
            "REJECTED": 0,
            "WAIT_RELEASE": 0,
            "CLOSED-关闭": 0
        }
        self.summary = ''

    def calcu_summary(self):
        rt_list = ["NO_FEEDBACK", "RESOLVED", "REJECTED", "WAIT_RELEASE", "CLOSED-关闭"]
        self.summary = super().summary(rt_list, "FAE_BUG Fixed: ")


class itemREQUIREMENT(KPIItem):
    def __init__(self):
        super().__init__()
        self.name_list = ["REQUIREMENT", "需求"]
        self.status_counter = {
            "RESOLVED": 0,
            "WAIT_FEEDBACK": 0,
            "NEW": 0,
            "DOING-进行中": 0,
            "ASSIGNED": 0,
            "PENDING": 0,
            "TESTING": 0,
            "REJECTED": 0,
            "WAIT_RELEASE": 0,
            "关闭": 0,
            "NO_FEEDBACK": 0
        }
        self.summary = ''

    def calcu_summary(self):
        rt_list = ["NO_FEEDBACK", "RESOLVED", "REJECTED", "WAIT_RELEASE", "关闭", "WAIT_FEEDBACK"]
        self.summary = super().summary(rt_list, "REQUIREMENT Completed: ")


class itemPROT_DEV(KPIItem):
    def __init__(self):
        KPIItem.__init__(self)
        self.name_list = ["PROTOCOL", "HF_PROTOCOL", "DEVELOP", "任务"]
        self.status_counter = {
            "NO_FEEDBACK": 0,
            "RESOLVED": 0,
            "CLOSED-关闭": 0,
            "WAIT_FEEDBACK": 0,
            "NEW-未开始": 0,
            "DOING-进行中": 0,
            "ASSIGNED": 0,
            "PENDING": 0,
            "TESTING": 0,
            "REJECTED": 0,
            "WAIT_RELEASE": 0,
            "FILED-已完成": 0
        }
        self.summary = ''

    def calcu_summary(self):
        rt_list = ["NO_FEEDBACK", "RESOLVED", "REJECTED", "WAIT_RELEASE", "CLOSED-关闭", "WAIT_FEEDBACK",
                   "FILED-已完成"]
        self.summary = super().summary(rt_list, "Protocol & Develop Complete: ")


class itemST_BUG(KPIItem):
    def __init__(self):
        KPIItem.__init__(self)
        self.name_list = ["ST_BUG", "HF_ST_BUG", "缺陷"]
        self.status_counter = {
            "NEW-待处理": 0,
            "UNCONFIRMED-待讨论": 0,
            "WAIT_SOLVE（待解决）": 0,
            "RESOLVED-已修复": 0,
            "LOG_Req": 0,
            "拒绝": 0,
            "CLOSED-关闭": 0,
            "REOPENED-重新打开": 0,
            "验证中": 0
        }
        self.summary = ''

    def calcu_summary(self):
        rt_list = ["拒绝", "RESOLVED-已修复", "CLOSED-关闭", "验证中"]
        self.summary = super().summary(rt_list, "ST_BUG Fixed: ")
        rt_list = ["REOPENED-重新打开"]
        self.summary += '\n' + super().summary(rt_list, "ST_BUG Reopened: ")


class KPIForOnePerson:
    def __init__(self):
        self.name = ''
        self.work_load = ""
        self.work_hour = 0
        self.fae_bug = itemFAEBUG()
        self.requirement = itemREQUIREMENT()
        self.prot_dev = itemPROT_DEV()
        self.st_bug = itemST_BUG()
        self.report = ""


members_in_team = [
    {"name": "Len.Liu", "name_CN": "刘信", "kpi": KPIForOnePerson()},
    {"name": "Claire.Liu", "name_CN": "刘慧", "kpi": KPIForOnePerson()},
    {"name": "Aleo.Liu", "name_CN": "刘洋洋", "kpi": KPIForOnePerson()},
    {"name": "Harper.Kuang", "name_CN": "匡婷", "kpi": KPIForOnePerson()},
    {"name": "Rain.Wu", "name_CN": "吴瑞", "kpi": KPIForOnePerson()},
    {"name": "Vincent.Cui", "name_CN": "崔子晨", "kpi": KPIForOnePerson()},
    {"name": "Bennett.Cui", "name_CN": "崔斌", "kpi": KPIForOnePerson()},
    {"name": "Haze.Zhang", "name_CN": "张仲俊", "kpi": KPIForOnePerson()},
    {"name": "Allen.Zhang", "name_CN": "张学忠", "kpi": KPIForOnePerson()},
    {"name": "Abert.Xu", "name_CN": "徐黎明", "kpi": KPIForOnePerson()},
    {"name": "Bear.Cao", "name_CN": "曹政", "kpi": KPIForOnePerson()},
    {"name": "Archie.Li", "name_CN": "李叶齐", "kpi": KPIForOnePerson()},
    {"name": "Arthur.Lee", "name_CN": "李永乐", "kpi": KPIForOnePerson()},
    {"name": "Walker.Wang", "name_CN": "汪自抒", "kpi": KPIForOnePerson()},
    {"name": "Elvin.Shen", "name_CN": "沈子扬", "kpi": KPIForOnePerson()},
    {"name": "Ying.Xiong", "name_CN": "熊鹰", "kpi": KPIForOnePerson()},
    {"name": "Ernie.Hu", "name_CN": "胡心月", "kpi": KPIForOnePerson()},
    {"name": "Todd.Zheng", "name_CN": "郑功良", "kpi": KPIForOnePerson()}
]


def get_file(path, file_list):
    # 列出当前目录下所有的文件夹和文件，返回一个列表
    inner_list = os.listdir(path)
    print(path)
    try:
        for inl in inner_list:
            # 过滤掉隐藏文件夹
            if inl[0] == '.' or inl[0] == '~':
                continue
            file_list.append(inl)
    except PermissionError:
        pass


row_attr_index = {
    "id": 0,
    "work_item_type": 0,
    "severity": 0,
    "title": 0,
    "status": 0,
    "person_in_charge": 0,
    "dead_line": 0,
    "estimated_man_hours": 0,
    "registered_man_hours": 0,
    "rest_man_hours": 0,
    "reopen_times": 0,
    "creator": 0,
    "creation_time": 0,
    "project": ""
}


# ['\ufeffID', '工作项类型', '严重程度', '标题', '状态', '负责人', '截止日期', '预估工时（小时）', '已登记工时（小时）', '剩余工时（小时）', '重新打开-停留次数', '创建者',
# '创建时间', '所属项目']
# ['\ufeff#', '跟踪', 'Severity', '主题', '状态', '指派给', '计划完成日期', '预估工时统计', '耗时', '预期时间', '作者', '创建于', '项目']
def init_row_index(row):
    row_attr_index["id"] = 0
    try:
        row_attr_index["work_item_type"] = row.index("工作项类型")
    except ValueError:
        print("error!!")
        row_attr_index["work_item_type"] = row.index("跟踪")
    r = row_attr_index["work_item_type"]
    print(f"work_item_type: {r}")

    try:
        row_attr_index["severity"] = row.index("严重程度")
    except ValueError:
        print("error!!")
        row_attr_index["severity"] = row.index("Severity")
    r = row_attr_index["severity"]
    print(f"severity: {r}")

    try:
        row_attr_index["title"] = row.index("标题")
    except ValueError:
        print("error!!")
        row_attr_index["title"] = row.index("主题")
    r = row_attr_index["title"]
    print(f"title: {r}")

    row_attr_index["status"] = row.index("状态")
    r = row_attr_index["status"]
    print(f"status: {r}")

    try:
        row_attr_index["person_in_charge"] = row.index("负责人")
    except ValueError:
        print("error!!")
        row_attr_index["person_in_charge"] = row.index("指派给")
    r = row_attr_index["person_in_charge"]
    print(f"person_in_charge: {r}")


def row_parser(row_list, first_row):
    if first_row:
        init_row_index(row_list)


def kpi_process(r_path, csv_list):
    report_string = ""
    for csv_file in csv_list:
        first_row = True
        fpath = os.path.join(r_path, csv_file)
        print(f"fpath: {fpath}, fn: {csv_file}")

        with open(fpath, 'r', encoding="utf-8") as csv_f:
            reader = csv.reader(csv_f)
            for r_list in reader:
                row_parser(r_list, first_row)
                first_row = False
                print(f"r_list: {r_list}")
                # report_string += r_list[0] + "\n"
                # row_parser(r_list, rattr)

    return report_string


def main():
    path = os.getcwd()
    root_path = path.replace("source", "kpi_data")
    print(f"root_path: {root_path}")
    # root_path = "D:\\myPyFun\\kpi_view\\kpi_data\\"
    kpi_csv_file_list = ["redmin_0101-0229.csv", "PMS_0101-0229.csv"]
    kpi_process(root_path, kpi_csv_file_list)

    # report_name = "2024Q1-KPI考勤报告.txt"
    # report = os.path.join(root_path, report_name)
    # with open(report, "w+") as f:
    #     f.write(report_head + '\n')
    #     f.write(report_main_seperator + '\n')
    #     f.write('\n')
    #     f.write()


# 外部调用的时候不执行
if __name__ == '__main__':
    main()
