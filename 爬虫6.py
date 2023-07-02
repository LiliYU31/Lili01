import requests
import json
import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class GetData:
    def __init__(self, dic, url):
        self.url = url
        self.dic = dic

    def get_url(self, lid, page, pageid=153):
        return self.url + "&lid=" + str(lid) + "&pageid=" + str(pageid) + "&page=" + str(page)

    def get_json_url(self, url):
        out = []
        json_req = requests.get(url)
        user_dict = json.loads(json_req.text)
        print(url)
        for dic in user_dict["result"]["data"]:
            out.append([dic["url"], dic['intro'], dic['title'], dic['ctime'], dic['media_name']])
        return out

    def getfind_data(self, list1, label):
        out_date = []
        for line in list1:
            try:
                req = requests.get(line[0])
                req.encoding = "utf-8"
                req = req.text
                content = re.findall('<p cms-style="font-L">(.*?)</p>', req, re.S)

                if len(line[0].split("/")[3]) == 10:
                    out_date.append([line[1], line[2], line[3], line[4], label, content[0]])

                elif len(line[0].split("/")[4]) == 10:
                    out_date.append([line[1], line[2], line[3], line[4], label, content[0]])

                elif len(line[0].split("/")[5]) == 10:
                    out_date.append([line[1], line[2], line[3], line[4], label, content[0]])

                elif len(line[0].split("/")[6]) == 10:
                    out_date.append([line[1], line[2], line[3], line[4], label, content[0]])
            except:
                pass
        return out_date

    def main(self):
        out_data_list = []  # 存放输入的数据
        for label, lid in self.dic.items():
            for page in range(1, 3):  # 爬取前2页的数据
                he_url = self.get_url(lid, page)
                json_url_list = self.get_json_url(he_url)
                output_data = self.getfind_data(json_url_list, label)
                out_data_list += output_data
        return out_data_list


data_dic = {"国内": 2510,
            "国际": 2511,
            "社会": 2669,
            "体育": 2512,
            "娱乐": 2513,
            "军事": 2514,
            "科技": 2515,
            "财经": 2516,
            "股市": 2517,
            "美股": 2518}

url = "https://feed.mix.sina.com.cn/api/roll/get?&k=&num=50"
get = GetData(data_dic, url)
news_data = get.main()


def funtion1(x):
    res1 = ''.join(re.findall('[\u4e00-\u9fa5]*["，","。","！","”","%","“","：","1","2","3","4","5","6","7","8","9","0"]',
                              x[20:]))
    res1 = res1.replace("\"", "")
    res1 = res1.replace("引文", "")
    res1 = res1.replace("正文", "")
    res1 = res1.replace("30003000", "")
    return res1


# 处理内容格式
for i in range(len(news_data)):
    news_data[i][-1] = funtion1(news_data[i][-1])

# 创建一个 Tkinter 窗口
root = tk.Tk()
root.geometry("800x600")

# 创建一个 Notebook 控件，并将其放置在窗口中
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# 创建导航栏
for label in data_dic.keys():
    frame = tk.Frame(notebook)
    notebook.add(frame, text=label)

    # 创建一个 Treeview 控件，并将其放置在 Frame 中
    treeview = ttk.Treeview(frame, columns=("标题", "日期", "来源"), show="headings")
    treeview.pack(fill=tk.BOTH, expand=True)

    # 设置表格的列标题
    treeview.heading("标题", text="标题")
    treeview.heading("日期", text="日期")
    treeview.heading("来源", text="来源")

    # 设置列的宽度
    treeview.column("标题", width=int(treeview.winfo_width() / 2))
    treeview.column("日期", width=int(treeview.winfo_width() / 4))
    treeview.column("来源", width=int(treeview.winfo_width() / 4))

    # 向 Treeview 控件中添加每篇新闻的标题、日期和来源
    for i in range(len(news_data)):
        if news_data[i][4] == label:
            treeview.insert("", tk.END, values=(news_data[i][1], news_data[i][2], news_data[i][3]))

    def show_full_title(event):
        if treeview.selection():
            item = treeview.selection()[0]
            title = treeview.item(item, "values")[0]
            date = treeview.item(item, "values")[1]
            source = treeview.item(item, "values")[2]
            messagebox.showinfo("完整标题与日期和来源", f"标题：{title}\n日期：{date}\n来源：{source}")

# 创建搜索按钮的点击事件
def search_news():
    keyword = entry.get()  # 获取文本框中的关键词
    search_result = []  # 存储匹配的新闻标题、时间和来源

    # 在news_data中搜索匹配的新闻
    for news in news_data:
        if keyword in news[1]:  # 如果关键词在新闻标题中
            search_result.append((news[1], news[2], news[3]))  # 添加匹配的新闻标题、时间和来源

    # 创建一个 Treeview 控件，并将其放置在主窗口中
    treeview = ttk.Treeview(root, columns=("标题", "日期", "来源"), show="headings")
    treeview.pack(fill=tk.BOTH, expand=True)

    # 设置表格的列标题
    treeview.heading("标题", text="标题")
    treeview.heading("日期", text="日期")
    treeview.heading("来源", text="来源")

    # 向 Treeview 控件中添加搜索结果
    for result in search_result:
        treeview.insert("", tk.END, values=result)

import collections

# 获取所有新闻标题
titles = [news[1] for news in news_data]

# 将所有标题拼接成一个字符串
all_titles = " ".join(titles)

# 使用正则表达式提取单词
words = re.findall(r'\w+', all_titles)

# 统计词频
word_counts = collections.Counter(words)

# 获取出现频率最高的前10个词
top_10_words = word_counts.most_common(10)

# 打印结果
for word, count in top_10_words:
    print(f"{word}: {count}")

# 创建主窗口
search_root = tk.Tk()
search_root.geometry("800x600")

# 创建一个 Treeview 控件，并将其放置在主窗口中
treeview = ttk.Treeview(search_root, columns=("标题", "日期", "来源"), show="headings")
treeview.pack(fill=tk.BOTH, expand=True)

# 设置表格的列标题
treeview.heading("标题", text="标题")
treeview.heading("日期", text="日期")
treeview.heading("来源", text="来源")

# 向 Treeview 控件中添加所有新闻的标题、日期和来源
for i in range(len(news_data)):
    treeview.insert("", tk.END, values=(news_data[i][1], news_data[i][2], news_data[i][3]))

# 创建搜索按钮的点击事件
def search_news():
    keyword = entry.get()  # 获取文本框中的关键词
    search_result = []  # 存储匹配的新闻标题、时间和来源

    # 在news_data中搜索匹配的新闻
    for news in news_data:
        if keyword in news[1]:  # 如果关键词在新闻标题中
            search_result.append((news[1], news[2], news[3]))  # 添加匹配的新闻标题、时间和来源

    # 清空Treeview控件中的内容
    treeview.delete(*treeview.get_children())

    # 向 Treeview 控件中添加搜索结果
    for result in search_result:
        treeview.insert("", tk.END, values=result)

# 创建一个文本框和一个搜索按钮，并将其放置在主窗口中
entry = tk.Entry(search_root, font=("Arial", 14))
entry.pack(pady=10)

search_button = tk.Button(search_root, text="搜索", font=("Arial", 14), command=search_news)
search_button.pack()

# 设置 Treeview 控件的列宽度
treeview.column("标题", width=300)
treeview.column("日期", width=150)
treeview.column("来源", width=150)

# 运行主循环
search_root.mainloop()


