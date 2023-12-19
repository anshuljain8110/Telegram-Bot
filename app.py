#telegram api
from telegram.ext import *

#connecting to db
from connectToDB import lend

#importing pandas
# import pandas
# df=pandas.read_csv("https://raw.githubusercontent.com/vikasjha001/telegram/main/qna_chitchat_professional.tsv",sep='/t')
# print(df)
# print(df.loc[df['Question'].str.lower() == "Do you ever get hurt?"])
# Loading env
import os
from dotenv import load_dotenv
load_dotenv()
TELETOKEN = os.environ.get('TELETOKEN')



async def start(update,context):
    await update.message.reply_text("hello")


async def list(update,context):
    st=""
    receivedData = lend.find({},{"_id":0})
    for x in receivedData:
        st+=f"{x['name']} - {x['amount']}\n"
    if(len(st)==0):
        st+="No Record Found"
    await update.message.reply_text(st)

    
async def entry(update,context):
    receivedData = update.message.text    # 'Anshul 100'
    receivedData = receivedData.replace("/entry","")
    receivedData = receivedData.upper()  # 'ANSHUL 100'
    receivedData = receivedData.split()  # ['ANSHUL','100']
    if(len(receivedData)==0):
        await update.message.reply_text("Provide Valid Entry")
        return
    receivedData[1]=int(receivedData[1]) # ['ANSHUL',100]

    a=lend.find_one({"name":receivedData[0]},{"_id":0})

    if(a):
        finalAmount = a['amount'] + receivedData[1]
        lend.find_one_and_update({"name":receivedData[0]},{'$set':{"amount":finalAmount}})
        await update.message.reply_text("Record Updated")
    else:
        lend.insert_one({"name":receivedData[0],"amount":receivedData[1]})
        await update.message.reply_text("Lender Created Or Updated")


async def message(update,context):
    await update.message.reply_text("I Don't Know How To Respond to: "+str(update.message.text))


if(__name__=="__main__"):
    app=Application.builder().token(TELETOKEN).build()


    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("list",list))
    app.add_handler(CommandHandler("entry",entry))
    app.add_handler(MessageHandler(filters.TEXT,message))


    app.run_polling()