## 仓库简介

* 微博热搜榜, 参数`wb`
* 百度热搜榜, 参数`bd`
* 360热点榜, 参数`360`
* csdn热榜接口, 下方查看
* 其他热搜待加入
测试
## 如何使用?

* 注册[vercel](https://vercel.com/)
* fork到你的仓库, 右上角
* 点击这里完成部署(一键部署)[![Vercel](https://img.shields.io/badge/vercel-%23000000.svg?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com/new/clone?s=https%3A%2F%2Fgithub.com%2FRr210%2Fhot_search.git)

## 请求参数

* vercel配置好的地址+`api?tit=`+参数(仓库简介有参数信息)
* `such as`: `https://hot-search.vercel.app/api?tit=wb`

### csdn 热榜

* 接口地址: `https://blog.csdn.net/phoenix/web/blog/hot-rank`
* 请求方式:`get`
* 请求参数:`page=x&pageSize=xx`
* `page`表示当前请求的页码 `pageSize`表示当前页码展示的文章数

## 转载须知

* 转载请标明出处
* 如果觉得我写的程序对你小有帮助, 可以点个⭐⭐

## :copyright: License

[![MIT](http://api.haizlin.cn/api?mod=interview&ctr=issues&act=generateSVG&type=a.svg)](https://github.com/Rr210/hot_search/blob/master/LICENSE) [![上一次提交](https://badgen.net/github/last-commit/Rr210/hot_search)]()
