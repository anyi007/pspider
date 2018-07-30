import pandas as pd
import math
import requests
import time


def get_json(url, num):
    my_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Host': 'www.lagou.com',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.lagou.com/jobs/list_python%E5%BC%80%E5%8F%91?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput=',
    }
    my_data = {
        'first': 'true',
        'pn': num,
        'kd': 'python开发'
    }
    res = requests.post(url, headers=my_headers, data=my_data)
    res.raise_for_status()
    res.encoding = 'utf-8'
    page = res.json()
    return page


def get_page_num(count):
    '''
    计算抓取的页数
    :param count:
    :return:
    '''
    res = math.ceil(count / 15)
    if res > 10:
        return 3
    else:
        return res


def get_page_info(jobs_list):
    page_info_list = []
    for i in jobs_list:
        job_info = []
        job_info.append(i.get('companyFullName'))  # 公司全称
        job_info.append(i.get('companyShortName'))  # 公司简称
        job_info.append(i.get('salary'))  # 薪资
        job_info.append(i.get('workYear',''))  # 工作经验
        job_info.append(i.get('education',''))  # 学历
        page_info_list.append(job_info)
    return page_info_list


def main():
    url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'
    while True:
        try:
            page = get_json(url, 1)
            total_count = page['content']['positionResult']['totalCount']
        except:
            pass
        else:
            print(page)
            break
    num = get_page_num(total_count)
    time.sleep(3)
    print('职位总数{}，页数{}'.format(total_count, num))
    total_info = []
    for n in range(1, num + 1):
        while True:
            try:
                page = get_json(url, n)
                job_list = page['content']['positionResult']['result']
            except:
                pass
            else:
                print(page)
                break
        page_info = get_page_info(job_list)
        total_info += page_info
        print('已经抓取了{}页，职位总数{}'.format(n, len(total_info)))
        time.sleep(5)
    df = pd.DataFrame(data=total_info, columns={'公司全称', '公司简称', '薪资', '工作经验', '学历'})
    df.to_csv('lagoujob.csv', index=False)
    print('保存完成')


if __name__ == '__main__':
    main()