import xlrd

"""
不管采用何种文件存储名单，要求返回如下格式内容即可。
list ['IEEE WIRELESS COMMUNICATIONS LETTERS', 'PEDIATRICS', 'BIRTH DEFECTS RESEARCH']
"""

# 读取 xlrd 格式的出版物名称文件，返回名称列表
def read_publication_names_file_xlrd(filename=""):
    dataset = []
    workbook = xlrd.open_workbook(filename)
    # 读第一张表 sheet
    table = workbook.sheets()[0]
    for row in range(table.nrows):
        # 跳过第一行
        if row > 0:
            # 读每一行的第零个元素
            dataset.append(table.row_values(row)[0])
    return dataset

def read_publication_names_file_text(filename=""):
    dataset = []
    with open(filename, encoding='utf-8') as f:
        read_rows = f.readlines()
        for a_row in read_rows:
            a_row = a_row.replace("\n","")
            dataset.append(a_row)
    return dataset

def read_highly_cited_author_names_txt(filename=""):
    dataset = []
    with open(filename, encoding='utf-8') as f:
        read_rows = f.readlines()
        for a_row in read_rows:
            a_row = a_row.replace("\n","")
            dataset.append(a_row)
    return dataset

if __name__=="__main__":
    #filename = "E:\web_of_science\input_task_file\publication_names.txt"
    #publication = read_publication_names_file_text(filename)
    #print(publication)

    filename = "E:\web_of_science\input_task_file\高引学者.txt"
    author = read_highly_cited_author_names_txt(filename)
    print(author)
    print(len(author))