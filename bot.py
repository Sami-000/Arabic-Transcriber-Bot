#-*- coding: utf-8 -*-
import time
from pyrogram import Client, filters
import os

app = Client(
    "speech_to_text_bot",
    api_id=123456,
    api_hash="abcd1234",
    bot_token="123456789:ABCDEFG1234-HIJKLMNO-PQrsTU"
)


received_files = 0

@app.on_message(filters.command('start'))
def start(client, message):
    client.send_message(message.chat.id, 'السلام عليكم، يمكنك إرسال ملف صوتي أو فيديو لتحويله إلى نص. \n\n سورس كود البوت:\n https://github.com/Sami-000/Arabic-Transcriber-Bot', disable_web_page_preview=True)

@app.on_message(filters.voice | filters.audio | filters.video)
def speech_to_text(client, message):
    global received_files

    # إرسال رسالة عدم إمكانية إستقبال اكثر من ٤ صوتيات في نفس الوقت
    if received_files >= 4:
        client.send_message(message.chat.id, ' هناك مجموعة من التحويلات يتم الآن. أرسل الصوتية بعد مدة -من فضلك- ', reply_to_message_id=message.id)
        return

    
    received_files += 1

    # إرسال رسالة تأكيد استلام الصوتية المرسلة من المستخدم
    progress_message = client.send_message(message.chat.id, 'جاري التحويل من الصوت إلى النص...', reply_to_message_id=message.id)

    # تحميل الملف الصوتي المرسل من المستخدم
    file_path = client.download_media(message)

    
    api_key = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' # هنا اكتب api wit.ai الخاص بك
    input_filename = file_path
    output_filename = f'{file_path}.txt'

    #  تحويل الصوت إلى نص عن طريق  wit.ai
    voice2txt = f'python3 speech.py {api_key} "{input_filename}" "{output_filename}"'
    os.system(voice2txt)
    #  تشكيل النص وتحويله إلى Docx
    txt2doc = f'python3 hkt_docx.py "{output_filename}" && rm -f "{output_filename}"'
    os.system(txt2doc)

    output_filename = f'{file_path}.docx'

    # إرسال الملف النصي النهائي إلى المستخدم
    client.send_document(message.chat.id, output_filename, reply_to_message_id=message.id)

    # حذف الملف الصوتي
    os.remove(file_path)
    # حذف الملف النصي 
    os.remove(output_filename)
    # حذف الرسالة التاكيد استلام الصوتية
    client.delete_messages(progress_message.chat.id, progress_message.id)

    
    received_files = 0

app.run()
