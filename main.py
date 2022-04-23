# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
from pytz import timezone
from telegram.ext import *
from telegram import *
import random
import pymongo
import logging

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

client = pymongo.MongoClient(
    "mongodb+srv://pugalkmc:pugalkmc@cluster0.ey2yh.mongodb.net/mydb?retryWrites=true&w=majority")

mydb = client.get_default_database()
#
TWO, THREE = range(2)
CHOOSE = range(1)

bot = Bot(token="5123712096:AAFoWsAeO_sJyrsl0upMa-LUCeHE-k8AWYE")
# ---------- functions ---------


def main_buttons(update, context):
    reply_keyboard = [['Do Task💸', '', 'Create Task📜'], ['Balance⚖', 'Deposit➕'], ['Referal link📎', 'More❕']]

    update.message.reply_text("Main Menu",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                               one_time_keyboard=True))


def start(update, context):
    sender = update.message.reply_text
    chat_id = update.message.chat_id
    username = update.message.chat.username
    text = update.message.text
    if str(username) == "None":
        sender("No username found for your account")
        sender("Please set username for your telegram\n"
               "1)Go telegram account settings\n"
               "2)Click username\n"
               "3)Set unique and simplified username")
    else:
        checking_exist = mydb["people"]
        bot.sendMessage(chat_id=chat_id, text="This KMC TRX earning bot"
                                              "\nYou can earn TRX by doing tasks"
                                              "\nAlso You can create task for other to do")

        main_buttons(update, context)
        for i in checking_exist.find({}):
            if username == i["username"]:
                break
        else:
            rand_num = random.randrange(11023648, 12023648)
            rand_text = random.choice('qwertyuiopasfghjklzxcvbnm')
            link = "https://telegram.me/earn_trx_ind_bot?start="+str(rand_num)+rand_text
            checking_exist.insert_one({"_id": chat_id, "username": username, "referal": link,
                                       "ref_count": 0, "TRX_balance": 0})
            bot.sendMessage(chat_id=1291659507, text="New user found @" + str(username))
            referal(text, username)


def referal(text, username):
    referal_link = text.replace("/start ", '')
    if len(referal_link) > 0:
        ref = mydb["people"]
        link = "https://telegram.me/earn_trx_ind_bot?start="+str(referal_link)
        try:
            get = ref.find_one({"referal": link})
            get_invitee = get["_id"]
            get_count = get["ref_count"]
            ref.update_one({"_id": get_invitee}, {"$set": {"ref_count": get_count+1}})
            bot.sendMessage(chat_id=get_invitee, text=f"You got new referal: @{username}")
        except:
            get = ref.find_one({"referal": "https://telegram.me/earn_trx_ind_bot?start=11299293i"})
            get_invitee = get["_id"]
            get_count = get["ref_count"]
            ref.update_one({"_id": get_invitee}, {"$set": {"ref_count": get_count+1}})


def msg_hand(update, context):
    chat_id = update.message.chat_id
    username = update.message.chat.username
    sender = update.message.reply_text
    text = update.message.text
    if 'Do Task💸' == text:
        task_list(update, context)
    elif 'Balance⚖' == text:
        pass
    elif 'Deposit➕' == text:
        bot.sendMessage(chat_id=chat_id, text="This is deposit option")
    elif 'Referal link📎' == text:
        get_link = mydb['people']
        get = get_link.find_one({"_id": chat_id})
        bot.sendMessage(chat_id=chat_id, text=f"Your referal link:\n{get['referal']}")
    elif "Withdraw➕" == text:
        pass

    if text == "More❕":
        reply_keyboard = [["Join Group❇","Withdraw➕" ], ["About💬","Rules🔖" ], ["Support👤","Back↩"]]
        sender("Use below buttons for quick access",
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True),
               reply_to_message_id=update.message.message_id)
    elif 'Rules🔖' == text:
        bot.sendMessage(chat_id=chat_id,text='''
        Task Manager Rules:

1. Please do not try to scam my bot :)
2. Do not create multiple accounts on the bot.
3. Do not advertise or promote anything illegal.
4. No porn, hyips, scams, scam bots.
5. All tasks need to be approved by admins.
6. Please do the tasks honestly and to the best of your ability.
7. Once a task has been broadcasted it can't be cancelled.
8. Funds deposited for tasks are non refundable.
9. All task buyers are resposible to check completed work.
10. Tasks are auto approved after 24 hours.

Users who try to scam the bot will be banned and lose all funds.''', reply_to_message_id=update.message.message_id)
    elif "About💬" == text:
        bot.sendMessage(chat_id=chat_id, text= ''''This bot allows anyone in the world to earn cryptocurrency completing simple tasks.

Earn TRX completing the tasks and uploading proof

Any type of task can be paid for - Deposit as little at 1 TRX

Describe the task - set payment per user and total budget

Users will complete tasks and send proof for you to approve

Hire thousands of real users cheap - get jobs done quick

Buy verified and gold users - get high quality workers

Tasks get broadcasted in many telegram channels

Promote affiliate programs and airdrops, referral systems

Hire people to make memes and graphics, upload and share them

Get users to upvote you on any site, follow, share your content''', reply_to_message_id=update.message.message_id)
    elif "Join Group❇" == text:
        bot.sendMessage(chat_id=chat_id, text="Soon available", reply_to_message_id=update.message.message_id)
    elif "Support👤" == text:
        bot.sendMessage(chat_id=chat_id, text="Admin support: @PugalKMC", reply_to_message_id=update.message.message_id)
    elif text == "Back↩" or text == "cancel":
        main_buttons(update, context)


def task_list(update, context):
    chat_id = update.message.chat_id
    tasks_list = mydb["tasks"]
    list1 = []
    total = 0
    for i in tasks_list.find({}):
        total += 1
        text = f"Task No: {total}\n" \
               f"Title: {i['title']}\n" \
               f"Do task : /{i['cmd_id']}\n" \
               f"Payment: {i['trx_per']} TRX\n" \
               f"Users : {i['done']}/{i['limit']}\n"

        list1.append(text)

    update.message.reply_text("Total task found:{0}\n\n{1}\n\n".format(total, '\n'.join(x for x in list1)))


def com():
    tasks_list = mydb["tasks"]
    task = ["empty"]
    for i in tasks_list.find({}):
        task.append(i["cmd_id"])
    return task


def do_task(update: Update, context: CallbackContext):
    message_id = update.message.message_id
    text = update.message.text
    text_id = text.replace("/", '')
    chat_id = update.message.chat_id
    context.user_data["task_id"] = text_id
    context.user_data["chat_id"] = chat_id
    find_task = mydb["tasks"]
    get = find_task.find_one({"cmd_id": text_id})
    # keyboard = [["Submit Task", "Skip Task"]]
    reply_markup = InlineKeyboardMarkup([[
        InlineKeyboardButton("Do task", callback_data="do"),
        InlineKeyboardButton("Close", callback_data="close")]])
    # reply_markup = ReplyKeyboardMarkup(keyboard,  one_time_keyboard=True , resize_keyboard=True)
    update.message.reply_text(f"Title: {get['title']}\n\n"
                              f"Description: {get['des']}\n\n"
                              f"Link: {get['link']}", reply_markup=reply_markup, timeout=10,
                              reply_to_message_id=message_id)


def task_select(update: Update, context: CallbackContext):
    if update.callback_query['data'] == "do":
        keyboard = [["Confirm Submit", "cancel"]]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.sendMessage(chat_id=context.user_data['chat_id'],
                        text=f"Now send your task proof and click submit\nThis proof will send to task owner for verification",
                        reply_markup=markup)
        return TWO
    else:
        bot.sendMessage(chat_id=context.user_data['chat_id'], text="Task Skipped")
        main_buttons(update, context)
        return ConversationHandler.END


def get_photo(update: Update, context: CallbackContext):
    context.user_data["photo"] = update.message.photo[-1]
    context.user_data["caption"] = update.message.caption
    update.message.reply_text("Got it!")
    return THREE
    # update.message.reply_photo(photo=photo)


def confirm_task(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if update.message.text == "Confirm Submit":
        tasks = mydb['tasks']
        get = tasks.find_one({"cmd_id": context.user_data['task_id']})
        get_list = list(get['pending'])
        permit_id = f"permit_{chat_id}"
        get_list.append(permit_id)
        bot.send_photo(chat_id=1291659507, photo=context.user_data['photo'], caption=f"{context.user_data['caption']}\n\nClick to approve-> /{permit_id}")
        tasks.update_one({"cmd_id":context.user_data['task_id']}, {'$set': {'pending': get_list}})
        update.message.reply_text("Got your response and sent to task owner for verification")
        main_buttons(update, context)
        return ConversationHandler.END
    else:
        main_buttons(update, context)
        return ConversationHandler.END


CREATE, TITLE, TRX_TOTAL, TRX_PER, LINK, CONFIRM = range(6)


def task_new(update, context):
    chat_id = update.message.chat_id
    people = mydb["people"]
    get = people.find_one({"_id": chat_id})
    if get["TRX_balance"] >= 1:
        markup = ReplyKeyboardMarkup([["cancel"]], one_time_keyboard=True, resize_keyboard=True)
        bot.sendMessage(chat_id=chat_id, text="Send task title to go next step:", reply_markup=markup,
                        reply_to_message_id=update.message.message_id)
        return CREATE
    else:
        bot.sendMessage(chat_id=chat_id, text="You must have atleat more than 1 TRX to create task\n"
                                              "To create task deposit TRX to the bot")
        return ConversationHandler.END


def get_title(update, context):
    chat_id = update.message.chat_id
    title = update.message.text
    context.user_data["title"] = title
    if title == "cancel":
        main_buttons(update, context)
        return ConversationHandler.END
    bot.sendMessage(chat_id=chat_id, text="Enter total task budget of TRX")
    return TITLE


def get_total(update, context):
    chat_id = update.message.chat_id
    trx_total = update.message.text
    balance = mydb["people"]
    get = balance.find_one({"_id": chat_id})
    if trx_total == "cancel":
        main_buttons(update, context)
        return ConversationHandler.END
    elif float(trx_total) >= 1:
        if get["TRX_balance"] >= float(trx_total):
            update.message.reply_text("Enter how many TRX per task for the user")
            context.user_data["trx_total"] = trx_total
            return TRX_TOTAL
        else:
            update.message.reply_text("Insufficient balance...\n"
                                      f"Your TRX balance {get['TRX_balance']}")
            return TITLE
    else:
        update.message.reply_text("TRX budget must be greater than 1")
        return TITLE


def get_per(update, context):
    chat_id = update.message.chat_id
    trx_per = update.message.text
    if trx_per == "cancel":
        main_buttons(update, context)
        return ConversationHandler.END
    elif float(trx_per) <= float(context.user_data["trx_total"]):
        if float(trx_per) > 0.3:
            update.message.reply_text("Send Task description")
            context.user_data["trx_per"] = trx_per
            return TRX_PER
        else:
            update.message.reply_text("Task amount can't be less than 0.3 TRX")
            return TRX_TOTAL


def description(update, context):
    chat_id = update.message.chat_id
    des = update.message.text
    trx_total = context.user_data["trx_total"]
    trx_per = context.user_data["trx_per"]
    title = context.user_data["title"]
    if des == "cancel":
        main_buttons(update, context)
        return ConversationHandler.END
    else:
        context.user_data["des"] = des
        update.message.reply_text("Send the link you want to promote")
        return LINK


def get_link(update, context):
    chat_id = update.message.chat_id
    link = update.message.text
    if link == "cancel":
        main_buttons(update, context)
        return ConversationHandler.END
    else:
        context.user_data["link"] = link
        markup = ReplyKeyboardMarkup([["Confirm", "cancel"]], one_time_keyboard=True, resize_keyboard=True)
        bot.sendMessage(chat_id=chat_id, text="Check task details once again and confirm:", reply_markup=markup)
        return CONFIRM


def sub_approve(title, trx_total, trx_per, link, des, chat_id):
    create_id = f"approve_{random.randint(100000,1000000)}"
    tasks = mydb['pending']
    cmd_id = f"task_{random.randint(100000,999999)}"
    ind_time = datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M')
    tasks.insert_one({"chat_id": chat_id, "create_id": create_id, "title": title, "trx_total": trx_total,
                      "trx_per": trx_per, "link": link, "des": des, "limit": int(trx_total//trx_per),
                      "time": ind_time, "done": 0, "cmd_id": cmd_id , 'done_by':[], 'pending':[]})
    bot.sendMessage(chat_id=1291659507, text=f"Task approve id:/{create_id}\n"
                                             f"Total budget: {trx_total}\n"
                                             f"TRX/user: {trx_per}\n"
                                             f"Users limit: {trx_total//trx_per}\n"
                                             f"title: {title}\n\n"
                                             f"Description:\n"
                                             f"{des}\n\n"
                                             f"link: {link}")


def confirm_create(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    if text == "Confirm":
        title = context.user_data["title"]
        trx_total = context.user_data["trx_total"]
        trx_per = context.user_data["trx_per"]
        link = context.user_data["link"]
        des = context.user_data["des"]
        sub_approve(title, float(trx_total), float(trx_per), link, des, int(chat_id))
        detect = mydb["people"]
        get = detect.find_one({"_id": chat_id})
        trx = get["TRX_balance"] - float(trx_total)
        detect.update_one({"_id": chat_id}, {"$set": {"TRX_balance": trx}})
        bot.sendMessage(chat_id=chat_id, text="Task submitted to owner")
        main_buttons(update, context)
        return ConversationHandler.END
    elif text == "cancel":
        main_buttons(update, context)
        return ConversationHandler.END
    else:
        return CONFIRM


def approve_list():
    cmd = mydb["pending"]
    cmds = ["nothing"]
    for i in cmd.find({}):
        cmds.append(i["create_id"])
    return cmds


def commands(update, context):
    text = update.message.text
    after = text.replace("/", '')
    tasks = mydb["tasks"]
    if "approve" in text:
        pending = mydb['pending']
        get = pending.find_one({"create_id": after})
        if str(get) != "None":
            tasks.insert_one(get)
            pending.delete_one({"create_id": after})
            update.message.reply_text("Task permitted successfully")
    elif "task" in text:
        get = tasks.find_one({'cmd_id':after})
        if str(get) != "None":
            do_task(update, context)
    elif "permit" in text:
        pass


def main():
    updater = Updater("5123712096:AAFoWsAeO_sJyrsl0upMa-LUCeHE-k8AWYE", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    task = ConversationHandler(entry_points=[CallbackQueryHandler(task_select)],
                               states={TWO: [MessageHandler(Filters.photo, get_photo)],
                                       THREE: [MessageHandler(Filters.text, confirm_task)]
                                       }, fallbacks=[MessageHandler(Filters.text, confirm_task)])

    add_task = ConversationHandler(entry_points=[MessageHandler(Filters.text("Create Task📜"), task_new)],
                                   states={CREATE: [MessageHandler(Filters.text, get_title)],
                                           TITLE: [MessageHandler(Filters.text, get_total)],
                                           TRX_TOTAL: [MessageHandler(Filters.text, get_per)],
                                           TRX_PER: [MessageHandler(Filters.text, description)],
                                           LINK: [MessageHandler(Filters.text, get_link)],
                                           CONFIRM: [MessageHandler(Filters.text, confirm_create)]
                                           }, fallbacks=[]
                                   )
    dp.add_handler(task)
    dp.add_handler(add_task)
    dp.add_handler(MessageHandler(Filters.command, commands))
    dp.add_handler(MessageHandler(Filters.text, msg_hand))
    updater.start_polling()
    updater.idle()


main()
