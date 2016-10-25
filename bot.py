#!/usr/bin/env python
# coding: utf-8

from wxbot import *
import ConfigParser
import json


class TulingWXBot(WXBot):
    def __init__(self):
        WXBot.__init__(self)

        self.tuling_key = "b9163e7460204c64a42457f6af701e1d"
        self.robot_switch = True
        self.robot_group = False
        self.robot_schedule = True
        self.robot_tiaoxi = False
        self.name = u"我的备忘录"
        self.who_can_with={}
        self.special_flag = True
        self.title = u'[Robot]'
        self.content = ''
        self.robot_title = False
        self.time_tick = 10
        self.only_one = ''
        self.only_reply = False
        
        try:
            cf = ConfigParser.ConfigParser()
            cf.read('conf.ini')
            self.tuling_key = cf.get('main', 'key')
        except Exception:
            pass
        print 'tuling_key:', self.tuling_key

    def tuling_auto_reply(self, uid, msg):
        if self.tuling_key:
            url = "http://www.tuling123.com/openapi/api"
            user_id = uid.replace('@', '')[:30]
            body = {'key': self.tuling_key, 'info': msg.encode('utf8'), 'userid': user_id}
            r = requests.post(url, data=body)
            respond = json.loads(r.text)
            result = u"机器人自动回复："
            if respond['code'] == 100000:
                result = respond['text'].replace('<br>', '  ')
            elif respond['code'] == 200000:
                result = respond['url']
            elif respond['code'] == 302000:
                for k in respond['list']:
                    result = result + u"【" + k['source'] + u"】 " +\
                        k['article'] + "\t" + k['detailurl'] + "\n"
            else:
                result = respond['text'].replace('<br>', '  ')

            print '    ROBOT:', result
            return result
        else:
            return u"知道啦"

    def auto_switch(self, msg):
        msg_data = msg['content']['data']
        stop_cmd = [u'退下', u'走开', u'关闭', u'关掉', u'休息', u'滚开',u'滚']
        stop_group = [u'关闭群']
        start_group = [u'开启群']
        start_cmd = [u'出来', u'启动', u'工作']
        start_tiaoxi = [u'调戏',u'调戏！']
        stop_tiaoxi = [u'停止调戏',u'关闭调戏']
        start_title = [u'开启标签',u'标签']
        stop_title = [u'关闭标签',u'停止标签']
        stop_special = [u'关闭特权',u'停止特权',u'对所有人回复']
        start_special = [u'开启特权',u'对特定人回复']
        to_name = self.get_contact_prefer_name(self.get_contact_name(msg['to_user_id']))
        if msg_data.find(u"只回复：")==0 :
            self.only_one = msg_data[4:]
            print '现在只回复：'
            print self.only_one
            self.send_msg_by_uid(u'[Robot]' + u'现在开始只回复'+self.only_one, msg['to_user_id'])
            self.only_reply = True
        
        
        if msg_data.find(u"停止只回复")!=-1 :
            self.only_reply = False
            self.send_msg_by_uid(u'[Robot]' + u'现在开始回复原状，不只回复'+self.only_one, msg['to_user_id'])
        if self.special_flag:
            for i in stop_special:
                if i == msg_data:
                    self.special_flag = False
                    self.send_msg_by_uid(u'[Robot]' + u'对所有人回复！', msg['to_user_id'])
        else:
            for i in start_special:
                if i == msg_data:
                    self.special_flag = True
                    self.send_msg_by_uid(u'[Robot]' + u'对特定人回复！', msg['to_user_id'])
        if self.robot_group:
            for i in stop_group:
                if i == msg_data:
                    self.robot_group = False
                    self.send_msg_by_uid(u'[Robot]' + u'回复群关闭！', msg['to_user_id'])
                        
        else:
            for i in start_group:
                if i == msg_data:
                    self.robot_group = True
                    self.send_msg_by_uid(u'[Robot]' + u'回复群开启！', msg['to_user_id'])
                
        if self.robot_switch:
            for i in stop_cmd:
                if i == msg_data:
                    self.robot_switch = False
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已关闭！', msg['to_user_id'])

    
        else:
            for i in start_cmd:
                if i == msg_data:
                    self.robot_switch = True
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已开启！', msg['to_user_id'])
        
        if self.robot_title:
            for i in stop_title:
                if i == msg_data:
                    self.robot_title = False
                    self.send_msg_by_uid(u'[Robot]' + u'标签已关闭！', msg['to_user_id'])
        
        else:
            for i in start_title:
                if i == msg_data:
                    self.robot_title = True
                    self.send_msg_by_uid(u'[Robot]' + u'标签已开启！', msg['to_user_id'])
                    self.title = u'[Robot]'

        
        for i in stop_tiaoxi:
            if i == msg_data:
                self.robot_tiaoxi = False
                self.send_msg_by_uid(u'[Robot]' + u'调戏已关闭！', msg['to_user_id'])
                
        for i in start_tiaoxi:
            if i == msg_data:
                self.robot_tiaoxi = True
                self.send_msg_by_uid(u'[Robot]' + u'调戏开启！', msg['to_user_id'])

        if msg_data.find(u"调戏")==0 and self.robot_tiaoxi:
            print '开始调戏'
            self.name = msg_data[msg_data.find(u"调戏")+2:]
            print self.name
        
        if msg_data.find(u"标签：")==0:
            self.title = msg_data[3:]
                
        if msg_data.find(u"内容：")==0:
            self.content = msg_data[3:]
        
        if msg_data == u"永久休眠":
            self.real_quit = True
            self.send_msg_by_uid(u'[Robot]' + u"机器人永久休眠！", msg['to_user_id'])
        
        if msg_data.find(u"时间间隔：")!= -1:
            time_tmp = msg_data[msg_data.find(u"时间间隔：")+5:]
            self.time_tick = int(time_tmp)
            self.send_msg_by_uid(u'[Robot]' + u"时间间隔已设定！", msg['to_user_id'])
            print self.time_tick

    def handle_msg_all(self, msg):
        stop_cmd = [u'退下', u'走开', u'关闭', u'关掉', u'休息', u'滚开',u'滚']
        start_cmd = [u'出来', u'启动', u'工作']
        
        name = self.get_contact_prefer_name(self.get_contact_name(msg['user']['id']))
        
        
        if not self.robot_switch and msg['msg_type_id'] != 1:
            return
        if msg['msg_type_id'] == 1 and msg['content']['type'] == 0:  # reply to self
            self.auto_switch(msg)
        elif msg['msg_type_id'] == 4 and msg['content']['type'] == 0:  # text message from contact
            if name not in self.watch_name:
                self.watch_name[name] = 0
                self.send_msg_by_uid(u'[Robot]' + u"您好，刘灿现在忙，若召唤机器人请回复“出来”，“启动”", msg['user']['id'])
            answer = self.title
            print name
            msg_data = msg['content']['data']
            if self.watch_name[name] :
                for i in stop_cmd :
                    if msg_data == i:
                        self.watch_name[name] = 0
                        self.send_msg_by_uid(u'[Robot]' + u"机器人已对您关闭！", msg['user']['id'])
            else :
                for i in start_cmd :
                    if msg_data == i:
                        self.watch_name[name] = 1
                        self.send_msg_by_uid(u'[Robot]' + u"机器人已对您开启，回复“滚”，“关闭”，“退下”等关闭机器人", msg['user']['id'])
            if not self.watch_name[name]:
                return

            elif self.watch_name[name] and self.special_flag and not self.only_reply:
                # print '搞事情啊，想回复？'
                if self.robot_title:
                    answer += self.tuling_auto_reply(msg['user']['id'], msg['content']['data'])
                    self.send_msg_by_uid(answer, msg['user']['id'])
                else:
                    self.send_msg_by_uid(self.tuling_auto_reply(msg['user']['id'], msg['content']['data']), msg['user']['id'])
            elif not self.special_flag and not self.only_reply:
                if self.robot_title:
                    answer += self.tuling_auto_reply(msg['user']['id'], msg['content']['data'])
                    self.send_msg_by_uid(answer, msg['user']['id'])
                else:
                    self.send_msg_by_uid(self.tuling_auto_reply(msg['user']['id'], msg['content']['data']), msg['user']['id'])
            elif self.only_reply:
                if name == self.only_one:
                    answer = self.tuling_auto_reply(msg['user']['id'], msg['content']['data'])
                    self.send_msg_by_uid(answer, msg['user']['id'])
        elif msg['msg_type_id'] == 4 and msg['content']['type'] == 6:
            if name not in self.watch_name:
                self.watch_name[name] = 0
                self.send_msg_by_uid(u'[Robot]' + u"您好，刘灿现在忙，若召唤机器人请回复“出来”，“启动”", msg['user']['id'])
            if self.watch_name[name] :
                self.send_msg_by_uid("😨,看不懂表情", msg['user']['id'])
        

        elif msg['msg_type_id'] == 3 and msg['content']['type'] == 0 and self.robot_group:  # group text message
            if 'detail' in msg['content']:
                my_names = self.get_group_member_name(self.my_account['UserName'], msg['user']['id'])
                if my_names is None:
                    my_names = {}
                if 'NickName' in self.my_account and self.my_account['NickName']:
                    my_names['nickname2'] = self.my_account['NickName']
                if 'RemarkName' in self.my_account and self.my_account['RemarkName']:
                    my_names['remark_name2'] = self.my_account['RemarkName']

                is_at_me = False
                for detail in msg['content']['detail']:
                    if detail['type'] == 'at':
                        for k in my_names:
                            if my_names[k] and my_names[k] == detail['value']:
                                is_at_me = True
                                break
                if is_at_me:
                    src_name = msg['content']['user']['name']
                    reply = u"Robot"+'  to' + src_name + ': '
                    if msg['content']['type'] == 0:  # text message
                        reply += self.tuling_auto_reply(msg['content']['user']['id'], msg['content']['desc'])
                    else:
                        reply += u"对不起，只认字，其他杂七杂八的我都不认识，,,Ծ‸Ծ,,"
                    self.send_msg_by_uid(reply, msg['user']['id'])
    def schedule(self):
        if self.robot_tiaoxi:
            self.send_msg(self.name, self.content)



def main():
    bot = TulingWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'

    bot.run()


if __name__ == '__main__':
    main()

