# 简介

更好用的可自定义 geosite，适用于 singbox

## 自定义规则文件

### custom-direct.txt

- 想要加入的直连列表
- 支持类型 `domain` `full` `regexp` `keyword`
  - 例如 `domain:baidu.com` `full:www.baidu.com`

### custom-direct-remove.txt

- 想要删除的直连列表
- 支持类型 `clear` `domain` `full` `regexp` `keyword`
- `clear` 会以关键词匹配删除
  - `clear:.google.com` 会删除 `a.google.com` `a.b.google.com`
  - `clear:google.com` 会删除 `google.com` `agoogle.com` `xxx.google.com`
- `domain` 会删除对应的域名
  - `domain:google.com` 仅会删除 `google.com`
- `full` `regexp` `keyword` 会删除对应的 `geosite` 规则
  - `full:nmsl.google.com` 会删除 `full:nmsl.google.com`