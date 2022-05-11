import re ,time ,requests
from pagermaid.listener import listener
from pagermaid.utils import alias_command ,obtain_message
def StrOfSize(size):
    def strofsize(integer, remainder, level):
        if integer >= 1024:
            remainder = integer % 1024
            integer //= 1024
            level += 1
            return strofsize(integer, remainder, level)
        elif integer < 0:
            integer = 0
            return strofsize(integer, remainder, level)
        else:
            return integer, remainder, level

    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    integer, remainder, level = strofsize(size, 0, 0)
    if level+1 > len(units):
        level = -1
    return ( '{}.{:>03d} {}'.format(integer, remainder, units[level]) )
@listener(is_plugin=True, outgoing=True, command=alias_command("subinfo"),
          description='获取机场订阅流量信息',parameters='<url>')
async def subinfo(context):
    headers = {
'User-Agent': 'ClashforWindows/0.18.1'
}
    url = await obtain_message(context)
    try:
        res=requests.get(url,headers=headers)
        if res.status_code == 200:
            try:
                info = res.headers['subscription-userinfo']
                info_num = re.findall('\d+',info)
                if len(info_num) == 4:
                    timeArray = time.localtime(int(info_num[3]))
                    dateTime = time.strftime("%Y-%m-%d", timeArray)                        
                    await context.edit(
                            '订阅链接：'+url+
                            '\n已用上行：`'+StrOfSize(int(info_num[0]))+
                            '`\n已用下行：`'+StrOfSize(int(info_num[1]))+ 
                            '`\n剩余流量：`'+StrOfSize(int(info_num[2])-int(info_num[1])-int(info_num[0]))+
                            '`\n最大流量：`'+StrOfSize(int(info_num[2]))+
                            '`\n到期时间：`'+dateTime+'`')
                else:
                    await context.edit(
                            '订阅链接：'+url+
                            '\n已用上行：`'+StrOfSize(int(info_num[0]))+
                            '`\n已用下行：`'+StrOfSize(int(info_num[1]))+ 
                            '`\n剩余流量：`'+StrOfSize(int(info_num[2])-int(info_num[1])-int(info_num[0]))+
                            '`\n最大流量：`'+StrOfSize(int(info_num[2]))+
                            '`\n到期时间：`无到期时间`')
            except:
                await context.edit('此订阅链接无流量信息')
        else:
            await context.edit('无法访问此订阅链接')
    except:
        await context.edit('参数错误，请重新输入')
