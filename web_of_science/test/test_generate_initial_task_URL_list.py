
import pickle

from WOS_settings import path_to_cookeis_pickle, path_to_task_url_info_list_pickle
from dependency_function import get_int_from_str
from dependency_function import generate_initial_task_URL_list

cookeis = pickle.load(open(path_to_cookeis_pickle, "rb"))
task_url_info_list = pickle.load(open(path_to_task_url_info_list_pickle, 'rb'))
print("task_url_info_list:\n", task_url_info_list)

for task_name, First_Paper_URL, last_page_num_index, last_paper_numbers in task_url_info_list:
    print("任务名：\t", task_name)
    last_page_num_index = get_int_from_str(last_page_num_index)
    last_paper_numbers = get_int_from_str(last_paper_numbers)
    number_of_high_quotations_possible = (last_page_num_index - 1) * 10 + last_paper_numbers
    initial_task_URL_list = generate_initial_task_URL_list(First_Paper_URL, last_page_num_index, last_paper_numbers)
    for task_url in initial_task_URL_list:
        print(task_url)