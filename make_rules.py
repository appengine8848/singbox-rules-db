import asyncio

import httpx

cn_domains_list = []
full_domains_list = []


async def url_get(url):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=30)
    return resp.text.strip()


def second_level_domain(domain):
    if domain.endswith(".cn"):
        return
    domain_list = domain.split(".")
    if len(domain_list) > 2:
        return ".".join(domain[-2:])
    else:
        return domain


async def cn_domains1():
    url = "https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/master/accelerated-domains.china.conf"
    cn_domains = await url_get(url)
    for domain in cn_domains.split("\n"):
        domain = second_level_domain(domain.split("/")[1])
        if domain:
            cn_domains_list.append(domain)


async def cn_domains2():
    url = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/ChinaMax/ChinaMax_Domain.txt"
    cn_domains = await url_get(url)
    for domain in cn_domains.split("\n"):
        domain_suffix = domain[0]
        if domain_suffix == ".":
            domain = second_level_domain(domain[1:])
            if domain:
                cn_domains_list.append(domain)
        elif domain_suffix != "#":
            full_domains_list.append("full:" + domain)


async def cn_domains3():
    url = "https://raw.githubusercontent.com/Loyalsoldier/domain-list-custom/release/cn.txt"
    cn_domains = await url_get(url)
    cn_domains = cn_domains.replace(":@cn", "")
    # 加入 custom-direct.txt 里的域名
    with open("custom-direct.txt", "r", encoding="utf-8") as file:
        cn_domains += "\n" + file.read().strip()
    for domain in cn_domains.split("\n"):
        domain_suffix = domain.split(":")[0]
        if domain_suffix == "domain":
            domain = second_level_domain(domain[7:])
            if domain:
                cn_domains_list.append(domain)
        elif domain_suffix in ("full", "regexp", "keyword"):
            full_domains_list.append(domain)


async def custom_direct_remove():
    all_list = []
    clear_list = []
    with open("custom-direct-remove.txt", "r", encoding="utf-8") as file:
        for domain in file:
            domain = domain.rstrip()
            domain_split = domain.split(":")
            domain_suffix = domain_split[0]
            domain_name = domain_split[-1]
            match domain_suffix:
                case "all":
                    all_list.append(domain_name)
                case "clear":
                    clear_list.append(domain_name)
                case "domain":
                    try:
                        cn_domains_list.remove(domain_name)
                        print(f"{domain_suffix} 规则已删除 {domain_name}")
                    except ValueError:
                        print(f"{domain_suffix} 规则未匹配 {domain_name}")
                case "full" | "regexp" | "keyword":
                    try:
                        full_domains_list.remove(domain)
                        print(f"{domain_suffix} 规则已删除 {domain}")
                    except ValueError:
                        print(f"{domain_suffix} 规则未匹配 {domain}")

    if clear_list or all_list:
        _cn_domains_list = cn_domains_list.copy()
        for domain in _cn_domains_list:
            for remove_domain in all_list:
                if remove_domain in domain:
                    cn_domains_list.remove(domain)
                    print(f"all 规则已删除 {domain}")
                    break 
            for remove_domain in clear_list:
                if remove_domain in domain:
                    cn_domains_list.remove(domain)
                    print(f"clear 规则已删除 {domain}")
                    break
    if all_list:
        _full_domains_list = full_domains_list.copy()
        for domain in _full_domains_list:
            for remove_domain in all_list:
                if remove_domain in domain:
                    full_domains_list.remove(domain)
                    print(f"all 规则已删除 {domain}")
                    break


async def main():
    # 添加 CN 域名
    await asyncio.gather(cn_domains1(), cn_domains2(), cn_domains3())
    # 去重排序
    global cn_domains_list
    global full_domains_list
    cn_domains_list = sorted(set(cn_domains_list), key=str.lower)
    full_domains_list = sorted(set(full_domains_list), key=str.lower)
    # 删除不需要的 CN 域名
    await custom_direct_remove()
    # 转为字符串
    direct_list = "\n".join(cn_domains_list) + "\n" + "\n".join(full_domains_list)
    # 写入到文件
    with open("direct-list.txt", "w") as file:
        file.write(direct_list)


if __name__ == "__main__":
    asyncio.run(main())
