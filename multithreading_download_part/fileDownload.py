import urllib.request
# import requests

# savepath = 'tmp/fs.rar'
# local_filename, headers = urllib.request.urlretrieve('https://getsamplefiles.com/download/rar/sample.rar', savepath)
# print(local_filename)


# url = 'https://getsamplefiles.com/download/rar/sample.rar'
#
# start = 0
# end = 1500
# headers = {'Range': 'bytes=%s-%s' % (start, end)}
#
# r = requests.get(url, headers=headers)
# print(r.status_code)

# print(r.headers)
# with open(savepath, 'wb') as outfile:
#     outfile.write(r.content)

#################################################################
import time
import requests

# url = 'https://getsamplefiles.com/download/rar/sample.rar'
url = 'https://figshare.com/ndownloader/files/9491434'
savepath = 'tmp/fs.rar'

t1 = time.time()

start = 0
end = 10485760
headers = {'Range': 'bytes=%s-%s' % (start, end)}

# r = requests.get(url, headers=headers)

r = requests.get(url, headers=headers)
print(r.status_code)
# with open(savepath, 'wb') as outfile:
#     outfile.write(r.content)

t2 = time.time()
print('run time:', t2-t1)



