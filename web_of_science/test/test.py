import pickle
from WOS_settings import path_to_task_url_info_list_pickle

from dependency_function import get_int_from_str,generate_initial_task_URL_list,get_first_and_del_first_item_from_list

task_url_info_list = pickle.load(open(path_to_task_url_info_list_pickle, 'rb'))
print(task_url_info_list)

for task_name, First_Paper_URL, last_page_num_index, last_paper_numbers in task_url_info_list:
    print("任务名：\t", task_name)
    last_page_num_index = get_int_from_str(last_page_num_index)
    last_paper_numbers = get_int_from_str(last_paper_numbers)

    initial_task_URL_list = generate_initial_task_URL_list(First_Paper_URL, last_page_num_index, last_paper_numbers)
    print(initial_task_URL_list)
    print('``````````````````')
    initial_task_URL_list = initial_task_URL_list[:100]
    a_url = get_first_and_del_first_item_from_list(initial_task_URL_list)
    while a_url is not None:
        print('正在处理{}'.format(a_url))
        a_url = get_first_and_del_first_item_from_list(initial_task_URL_list)