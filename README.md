# 这是什么

家用监控，使用树莓派监控家中是否进入陌生人。一旦发现陌生人脸，保存下照片，并通过钉钉通知主人（自己）。

# 什么原理

>使用树莓派+摄像头定时采集图片

>opencv识别图中是否有人脸

>如果发现有人脸

>>存下图片

>>调用face++ api判断是否是自己人

>>如果不是自己人

>>>调用钉钉机器人webhook发送消息

# 怎么运行

1. 配置 settings.conf
- facepp下需要配置face++的key和secret。
- 用于对比人脸的faceset_token和测试用的face_id是中间步骤，运行监控程序时不会用到。
- dingtalk下需要配置钉钉群机器人的web hook，[钉钉群机器人文档](https://open-doc.dingtalk.com/docs/doc.htm?spm=a219a.7629140.0.0.karFPe&treeId=257&articleId=105735&docType=1)

2. 入口参考 start.sh

# 参考资料：
1. [树莓派刷Raspian系统,ssh,vnc](https://www.jianshu.com/p/104931224f1a)
2. [更换清华源](https://www.jianshu.com/p/67b9e6ebf8a0)
3. [树莓派配置opencv环境](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/)
4. [使用opencv摄像头检测人脸](https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2650738591&idx=1&sn=68f8ec3e540eb0d7ca600dc7f52955f9&chksm=871acbe1b06d42f72a05a3441bf4f11960ca121545d5608d6166f998ce1dce68e6b5e1832c9c&mpshare=1&scene=1&srcid=030449pkXRNPQxelYcujzlFp#rd)
5. [使用face++提升识别准确度](https://blog.csdn.net/qq_37588821/article/details/80633563)
6. [face++ api文档](https://console.faceplusplus.com.cn/documents/4888391)
