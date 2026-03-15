import urllib.request
import os

media = [
    ("https://media.licdn.com/dms/image/v2/D5622AQG7fEs1MGI1GA/feedshare-shrink_1280/B56ZYvwe92GUAk-/0/1744557962659?e=2147483647&v=beta&t=HSKIXEGlS7kjjGgXl3BFYEiEVjrFkGyvDTjcbtvow0Q", "us_mortality_preview.jpg"),
    ("https://dms.licdn.com/playlist/vid/v2/D5605AQECBhK7MTuUCw/mp4-720p-30fp-crf28/B56ZYqP27DGcBo-/0/1744465537331?e=2147483647&v=beta&t=gFqomOsovp0KaQNGNfInD2GLptDI55_KPwi9LufnePg", "excel_analytic_preview.mp4")
]

for url, filename in media:
    print(f"Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"Successfully downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
