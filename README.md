# Markdown-Scripts
一些常用的MarkDown文档整理小工具，配合typora等本地markdown笔记软件食用更佳！



### 常用的脚本工具

- **cleanerWork** 

  这是一个能够解决 Typora 在编辑的过程中，因为用户取消插入文件导致的图片资源产生垃圾的问题，使用该脚本会清理没有被文件使用的图片，并且将未使用的图片放到 clean 文件夹中以供找回，以免误删。

  使用方法: .md 文件以及资源文件放置到 solve 文件夹中，使用 python (python 3) 运行 此文件夹下的 python 文件。

  

- **downloadWork**

  这是一个专门为markdown设计的图片下载器，能够将原本是在 CDN 上的图片转移到本地，以免因为图床的失效，导致了图片的丢失，或者是本身是语雀、飞书等平台导出的文件想要将图片下载到本地的一个小工具。

  使用方法: 将 .md 文件放到 solve 文件夹下，使用 python (python 3) 运行当前目录的 python 文件即可。 图片将会保存到本地的 `文件名.assets/` 文件夹下。

  

- **packageWork**

  这是一个专门为markdown设计的文件打包工具，会将单独的 markdown 文件以及 markdown 文件所引用的资源文件一起压缩成一个压缩包，以便于文件的分享、导出和上传。

  使用方法: 将 .md 文件放到 old 文件夹下，使用 python (python 3) 运行当前目录的 python 文件即可。 将会生成与你的md文件相同的压缩包。

  

- **renameWork**

  这是将资源文件夹 xxx.assets 进行命名的工具，他会根据你的markdown文件名对文件夹进行重命名，还会将markdown 中对图片的引用修改为新的文件夹，针对想修改名字但是奈何md文件已经命名了的情况。

  使用方法: 将 .md 文件放到 old 文件夹下，使用 python (python 3) 运行当前目录的 python 文件即可。 



如果有更多的需求或者脚本有bug，请提出issue，如果脚本帮助了你，请为这个项目点一个star!
