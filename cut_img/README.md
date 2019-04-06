# 图像分割模块

[TOC]



利用截屏中含有标准的提示窗口这一特点，将窗口截取出来，生成较小的图片

**接口可以表述如下：**

```python
def get_window_set(img_path):
    ...
    #window_set 表述识别出来的窗口图片
    return window_set
```

