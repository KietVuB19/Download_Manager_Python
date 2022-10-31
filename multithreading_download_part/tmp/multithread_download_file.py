import threading
import multiprocessing
import requests
import time

url = 'https://figshare.com/ndownloader/files/9491434'
savepath = 'tmp/fs.rar'
chunksize = 10485760 // 10
threads = []
parts = {}


def download(start):
    headers = {'Range': 'bytes=%s-%s' % (start, start + chunksize)}
    req = requests.get(url, headers=headers)
    parts[start] = req.content


if __name__ == '__main__':
    # Initialize threads
    t1 = time.time()
    for i in range(10):
        t = multiprocessing.Process(target=download, args=(i * chunksize,))
        t.start()
        threads.append(t)

    # Join threads back (order doesn't matter, you just want them all)
    for i in threads:
        i.join()

    t2 = time.time()
    # Sort parts and you're done
    print('time:', t2 - t1)
