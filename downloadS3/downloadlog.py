import os
import boto3


s3 = boto3.resource('s3')
print("输入时间（空格）用户id，例如：2021-02-20 57ea449d7748abb7428b456a")
while True:
    t_u = input().split()
    print(t_u)
    download_path = '/Users/pof/Downloads/feedback/'  # 修改为自己的保存路径
    log = 'wooplus-prod-client-log'
    t = '/' + t_u[0]
    user_id = '/' + t_u[1]
    Prefix = 'logs' + t + user_id
    my_bucket = s3.Bucket(log)
    list= []
    dir = ""
    for obj in my_bucket.objects.filter(Prefix=Prefix):
        dir = download_path + obj.key[:len('logs/2021-02-20/')]
        if not os.path.exists(dir):
            os.makedirs(dir)
            os.makedirs(dir + t_u[1] + "_sql")
        if obj.key not in list and obj.key[-3:] != "txt":
            list.append(obj.key)
    list.reverse()
    list_download = []   # 存要下载的文件名
    list_after = []   # 存后缀用于去重
    for i in list:   # 进行去重，去重后的文件名加入到要下载的数组中
        if i[-2:] not in list_after:
            list_after.append(i[-2:])
            list_download.append(i)
    if len(list_download) == 0:
        print("未获取到日志，可能日志上传失败，重新输入新的日期和id")
        continue
    if len(list_download) >= 10:
        print("日志上传大于10")
        continue
    for i in list_download:
        s3.Bucket("wooplus-prod-client-log").download_file(i, download_path + i)
    zip_name = download_path + list_download[0][:-2]
    zip_path = dir
    os.system("cat " + zip_name + ".* > " + zip_name)
    zip_commend = "unzip -o " + zip_name + " -d " + zip_path + t_u[1] + "_sql"
    os.system(zip_commend)
    os.system("rm -f " + zip_name + ".*")
    os.system("rm -f " + zip_name)
    print("解压完成，可进行下一个用户的操作")
    # 2021-04-22 6080defd26bc0cf81a0b53ab