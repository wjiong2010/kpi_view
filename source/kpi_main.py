import os
import csv

folder_name = [
    "刘信Len.Liu",
    "刘慧Claire.Liu",
    "刘洋洋Aleo.Liu",
    "匡婷Harper.Kuang",
    "吴瑞Rain.Wu",
    "崔子晨Vincent.Cui",
    "崔斌Bennett.Cui",
    "张仲俊Haze.Zhang",
    "张学忠Allen.Zhang",
    "徐黎明Abert.Xu",
    "曹政Bear.Cao",
    "李叶齐Archie.Li",
    "李永乐Arthur.Lee",
    "汪自抒Walker.Wang",
    "沈子扬Elvin.Shen",
    "熊鹰Ying.Xiong",
    "胡心月Ernie.Hu",
    "郑功良Todd.Zheng"
]

ROW_ATTRIBUTE_INDEX = {
    "ID": 0,
    "Status": 0,
    "Type": 0
}

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
        rt_list = ["NO_FEEDBACK", "RESOLVED", "REJECTED", "WAIT_RELEASE", "CLOSED-关闭", "WAIT_FEEDBACK", "FILED-已完成"]
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


fae_bug = itemFAEBUG()
requirement = itemREQUIREMENT()
prot_dev = itemPROT_DEV()
st_bug = itemST_BUG()


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


def row_parser(row_list, attr):
    id_v = row_list[attr["ID"]]
    st = row_list[attr["Status"]]
    ty = row_list[attr["Type"]]

    if ty in fae_bug.name_list:
        fae_bug.do_proc(id_v, st, ty)
        fae_bug.calcu_summary()
        return 0
    if ty in requirement.name_list:
        requirement.do_proc(id_v, st, ty)
        requirement.calcu_summary()
        return 0
    if ty in prot_dev.name_list:
        prot_dev.do_proc(id_v, st, ty)
        prot_dev.calcu_summary()
        return 0
    if ty in st_bug.name_list:
        st_bug.do_proc(id_v, st, ty)
        st_bug.calcu_summary()
        return 0


def kpi_process(r_path, rattr=None):
    if rattr is None:
        rattr = ROW_ATTRIBUTE_INDEX
    file_list = []
    fae_bug.reset()
    requirement.reset()
    prot_dev.reset()
    st_bug.reset()
    get_file(r_path, file_list)

    for fn in file_list:
        if "pms.csv" == fn:
            rattr["ID"] = 0
            rattr["Status"] = 2
            rattr["Type"] = 13
        elif "redmin_BUG.csv" == fn:
            rattr["ID"] = 0
            rattr["Status"] = 3
            rattr["Type"] = 2
        elif "redmin_FAE.csv" == fn:
            rattr["ID"] = 0
            rattr["Status"] = 3
            rattr["Type"] = 2
        fpath = os.path.join(r_path, fn)
        print(f"fpath: {fpath}, fn: {fn}")
        # src_book = xlrd.open_workbook(fpath)
        # src_sheet = src_book.sheet_by_index(0)
        with open(fpath, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            for r_list in reader:
                row_parser(r_list, rattr)
        # xlsx_parser(src_sheet)
    report_string = fae_bug.get_info() + '\n'
    report_string += prot_dev.get_info() + '\n'
    report_string += requirement.get_info() + '\n'
    report_string += st_bug.get_info() + '\n\n'

    report_string += report_secondary_seperator + '\n'
    report_string += report_summary + '\n'
    report_string += "    Workload:" + '\n'
    report_string += fae_bug.summary + '\n'
    report_string += requirement.summary + '\n'
    report_string += st_bug.summary + '\n'
    report_string += prot_dev.summary + '\n'

    return report_string


def main():
    root_path = "E:\\weekly_report\\2023\\2023-4-KPI"
    report_name = "2023Q4-KPI考勤报告.txt"
    report = os.path.join(root_path, report_name)
    with open(report, "w+") as f:
        f.write(report_head + '\n')
        for fd in folder_name:
            f.write(report_main_seperator + '\n')
            f.write(fd)
            f.write('\n')
            p = os.path.join(root_path, fd)
            f.write(kpi_process(p))


# 外部调用的时候不执行
if __name__ == '__main__':
    main()
