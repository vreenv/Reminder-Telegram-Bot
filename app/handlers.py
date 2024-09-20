from aiogram import Router, types, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from app.texts import texts, welcome_message, hlp
import app.keyboards as kb
import pytz
from pytz import all_timezones, timezone
from datetime import datetime, timedelta
import asyncio
import re
import json

router = Router()
TOKEN = json.load(open("app/config/config.json"))['tg_token']
bot = Bot(TOKEN)

user_languages = {}
user_timezones = {}
reminders = {}


@router.message(Command('start'))
async def start(message: Message):
    await message.answer('Choose bot language, please', reply_markup=kb.lang)


@router.message(Command('help'))
async def hp(message: Message):
    await message.answer(hlp[user_languages[message.chat.id]])


@router.message(lambda message: message.text in ["English", "Čeština"])
async def set_language(message: types.Message):
    """Nastavení jazyku a welcome message"""
    user_languages[message.chat.id] = message.text
    await message.answer(welcome_message[user_languages[message.chat.id]],
                         reply_markup=ReplyKeyboardRemove())


@router.message(Command('change_lang'))
async def change_lang(message: types.Message):
    """Změna jazyku"""
    if user_languages[message.chat.id] == 'English':
        user_languages[message.chat.id] = 'Čeština'
        await message.answer(f"{texts[user_languages[message.chat.id]]['change_lang']} Čeština.")
    elif user_languages[message.chat.id] == 'Čeština':
        user_languages[message.chat.id] = 'English'
        await message.answer(f"{texts[user_languages[message.chat.id]]['change_lang']} English.")


@router.message(Command('change_tz'))
async def change_tz(message: types.Message):
    """Změna časového pásma"""
    tz = message.text.split('/change_tz', 1)[1].strip()
    if tz in all_timezones:
        if user_timezones[message.chat.id] == tz:
            await message.answer(f"{texts[user_languages[message.chat.id]]['no_change_tz']} ({tz}).\n")
        else:
            user_timezones[message.chat.id] = tz
            user_timezone = timezone(tz)
            current_time = datetime.now(user_timezone)
            await message.answer(f"{texts[user_languages[message.chat.id]]['change_tz']} ({tz}).\n"
                                 f"{texts[user_languages[message.chat.id]]['cur_time']}\n"
                                 f"{current_time.strftime('%d.%m.%Y\n%H:%M:%S')}")
    else:
        await message.reply(texts[user_languages[message.chat.id]]['invalid_tz'])


@router.message(lambda message: message.text in all_timezones)
async def set_timezone(message: Message):
    """Nastavení časového pásma uživatele"""
    user_tz = message.text
    user_timezone = timezone(user_tz)
    current_time = datetime.now(user_timezone)
    user_timezones[message.chat.id] = message.text
    await message.answer(f"{texts[user_languages[message.chat.id]]['location_set']} ({user_tz}).\n"
                         f"{texts[user_languages[message.chat.id]]['cur_time']}\n"
                         f"{current_time.strftime('%d.%m.%Y\n%H:%M:%S')}")


@router.message(Command('reminder'))
async def set_reminder(message: types.Message):
    """Nastavení připomínky podle formátu zprávy uživatele"""
    user_tz = user_timezones.get(message.chat.id)

    if not user_tz:
        await message.answer(texts[user_languages[message.chat.id]]['not_set'])
        return

    try:
        message_text = message.text.split(' ', 1)[1]
        pattern_a = r'(\d{2}:\d{2} \d{2}\.\d{2}\.\d{4})'
        pattern_b = r'(\d{2}:\d{2})'
        match_a = re.search(pattern_a, message_text)
        match_b = re.search(pattern_b, message_text)
        if match_a:
            split_index = match_a.start()
            task_text = message_text[:split_index].strip()
            date_time_str = message_text[split_index:].strip()
            user_time = datetime.strptime(date_time_str, '%H:%M %d.%m.%Y')

            user_timezone = timezone(user_tz)
            user_local_time = user_timezone.localize(user_time)
            utc_time = user_local_time.astimezone(pytz.utc)

            if utc_time < datetime.now(pytz.utc):
                await message.answer(texts[user_languages[message.chat.id]]['error'])
                return

            reminders.setdefault(message.chat.id, []).append({"text": task_text, "utc_time": utc_time})
            await message.answer(f"{texts[user_languages[message.chat.id]]['reminder_set']} "
                                 f"{user_local_time.strftime('%d.%m.%Y %H:%M:%S')} UTC.")

            await schedule_reminder(message.chat.id, utc_time, task_text)

        elif texts[user_languages[message.chat.id]]['tmrw'] in message_text.lower():
            split_index = message_text.lower().find(texts[user_languages[message.chat.id]]['tmrw'])
            task_text = message_text[:split_index].strip()
            time_str = re.search(pattern_b, message_text[split_index:]).group()

            tomorrow = datetime.now() + timedelta(days=1)
            date_time_str = f"{time_str} {tomorrow.strftime('%d.%m.%Y')}"

            user_time = datetime.strptime(date_time_str, '%H:%M %d.%m.%Y')

            user_timezone = timezone(user_tz)
            user_local_time = user_timezone.localize(user_time)
            utc_time = user_local_time.astimezone(pytz.utc)

            if utc_time < datetime.now(pytz.utc):
                await message.answer(texts[user_languages[message.chat.id]]['error'])
                return

            reminders.setdefault(message.chat.id, []).append({"text": task_text, "utc_time": utc_time})
            await message.answer(f"{texts[user_languages[message.chat.id]]['reminder_tomorrow']} "
                                 f"{user_local_time.strftime('%H:%M')} UTC.")

            await schedule_reminder(message.chat.id, utc_time, task_text)

        elif match_b:
            split_index = match_b.start()
            task_text = message_text[:split_index].strip()
            time_str = message_text[split_index:].strip()

            current_date = datetime.now().strftime('%d.%m.%Y')
            date_time_str = f"{time_str} {current_date}"

            user_time = datetime.strptime(date_time_str, '%H:%M %d.%m.%Y')

            user_timezone = timezone(user_tz)
            user_local_time = user_timezone.localize(user_time)
            utc_time = user_local_time.astimezone(pytz.utc)

            if utc_time < datetime.now(pytz.utc):
                await message.answer(texts[user_languages[message.chat.id]]['error'])
                return

            reminders.setdefault(message.chat.id, []).append({"text": task_text, "utc_time": utc_time})
            await message.answer(f"{texts[user_languages[message.chat.id]]['reminder_today']} "
                                 f"{user_local_time.strftime('%H:%M')} UTC.")

            await schedule_reminder(message.chat.id, utc_time, task_text)

    except Exception as e:
        await message.answer(f"Error: {str(e)}. Set time and date in a format 'HH:MM DD.MM.YYYY'.")


@router.callback_query(lambda call: call.data.startswith("delay_"))
async def delay_reminder(callback_query: CallbackQuery):
    """Odložení připomínky o interval času, zvolený uživatelem"""
    chat_id = callback_query.message.chat.id
    data = callback_query.data.split("_")
    delay_type = data[1]
    user_tz = user_timezones.get(chat_id)

    await callback_query.answer()

    if chat_id in reminders and reminders[chat_id]:
        current_reminder = reminders[chat_id][-1]

        delay_mapping = {
            "10min": timedelta(minutes=10),
            "30min": timedelta(minutes=30),
            "1hour": timedelta(hours=1),
            "1day": timedelta(days=1)
        }

        delay = delay_mapping.get(delay_type)
        if delay:
            for reminder in reminders[chat_id]:
                utc_time = reminder["utc_time"]

                user_timezone = timezone(user_tz)
                local_time = utc_time.astimezone(user_timezone)
                new_reminder_time = local_time + delay

                if reminder['utc_time'] == current_reminder['utc_time']:
                    reminder['utc_time'] = new_reminder_time

                    await bot.send_message(chat_id, f"{texts[user_languages[chat_id]]['delay_by']} "
                                                    f"{delay}.\n\n"
                                                    f"{texts[user_languages[chat_id]]['new_time']} "
                                                    f"{new_reminder_time.strftime('%d.%m.%Y %H:%M:%S')} UTC.")
                    await schedule_reminder(chat_id, new_reminder_time, current_reminder['text'])

    else:
        await bot.send_message(chat_id, texts[user_languages[chat_id]]['error_2'])


@router.callback_query(lambda call: call.data == "delete")
async def delete_reminder(callback_query: CallbackQuery):
    """Smazání připomínky ze slovníku reminders"""
    chat_id = callback_query.message.chat.id

    if chat_id in reminders and reminders[chat_id]:
        current_reminder = reminders[chat_id][-1]

        reminders[chat_id].remove(current_reminder)
        if not reminders[chat_id]:
            del reminders[chat_id]

        await bot.send_message(chat_id, texts[user_languages[chat_id]]['del'])
    else:
        await bot.send_message(chat_id, texts[user_languages[chat_id]]['error_2'])

    await callback_query.answer()


async def schedule_reminder(chat_id, reminder_time, task_text):
    now = datetime.now(pytz.utc)
    delay = (reminder_time - now).total_seconds()

    if delay > 0:
        await asyncio.sleep(delay)
        await bot.send_message(chat_id, f"{texts[user_languages[chat_id]]['reminder']} "
                                        f"{task_text}\n\n{texts[user_languages[chat_id]]['delay']}",
                               reply_markup=kb.kbs[user_languages[chat_id]])
    else:
        await bot.send_message(chat_id, texts[user_languages[chat_id]]['error'])


@router.message(Command('list'))
async def list_reminders(message: types.Message):
    """Zobrazení seznamu všech aktuálních připomínek"""
    user_id = message.chat.id
    user_tz = user_timezones.get(user_id)

    if user_id not in reminders or not reminders[user_id]:
        await message.answer(texts[user_languages[message.chat.id]]['error_2'])
        return

    reminder_list = []
    for reminder in reminders[user_id]:
        task = reminder["text"]
        utc_time = reminder["utc_time"]

        user_timezone = timezone(user_tz)
        local_time = utc_time.astimezone(user_timezone)

        time_str = local_time.strftime('%d.%m.%Y %H:%M:%S')
        reminder_list.append(f"{texts[user_languages[message.chat.id]]['task']}"
                             f" {task}\n{texts[user_languages[message.chat.id]]['time']} {time_str}")

    await message.answer("\n\n".join(reminder_list))


@router.message(lambda message: message.chat.id not in user_timezones)
async def invalid_timezone(message: Message):
    """Pokud poloha uživatele je neplatná,
    pošle odpovídající zprávu"""
    await message.reply(texts[user_languages[message.chat.id]]['invalid_tz'])
