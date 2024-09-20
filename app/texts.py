welcome_message = {'Čeština': """
Vítejte u Bota na připomínky! Zde je návod, jak ho používat:

- Pro nastavení připomínky na dnešek napište:
  `/reminder Úkol Čas`
  Příklad: `/reminder Jóga 18:00`

- Pro nastavení připomínky na zítra použijte:
  `/reminder Úkol zítra Čas`
  Příklad: `/reminder Matematika zítra 12:00`

- Pro nastavení připomínky na konkrétní datum napište:
  `/reminder Úkol Čas Datum`
  Příklad: `/reminder Zasedání 09:00 24.08.2024`

Použijte příkaz /help pro další informace.

To je vše! Pošlete prosím svoji polohu ve formátu Continent/City (v angličtině, prosím), abych mohl nastavit Vaše časové pásmo.
""",
                   'English': """
Welcome to the Reminder Bot! Here's how to use it:

- To set a reminder for today, use:
  `/reminder Task Time`
  Example: `/reminder Math homework 22:00`

- To set a reminder for tomorrow, use:
  `/reminder Task tomorrow Time`
  Example: `/reminder Meeting tomorrow 12:00`

- To set a reminder for a specific date, use:
  `/reminder Task Time Date`
  Example: `/reminder Swimming pool 09:00 24.08.2024`

Use /help command for more information.

That's it! Now, send me your location in the format Continent/City, so I could set your timezone.
"""}


texts = {
    'English': {
        'set_language': "Your language is set to",
        'language_set': "Your language is already set to",
        'change_lang': "Language is changed to",
        'location_set': "Your location is set to",
        'change_tz': "Your location is changed to",
        'no_change_tz': "Your location is already set to",
        'cur_time': "Current time in your timezone:\n",
        'invalid_tz': "Your location is invalid. Try again.",
        'not_set': "At first set your location.",
        'reminder_set': "Reminder is set on",
        'reminder_today': "Reminder is set for today at",
        'reminder_tomorrow': "Reminder is set for tomorrow at",
        'choose_time': "Please, choose the time for your reminder.",
        'reminder': "Reminder:",
        'error': "Error: reminder is set on a past time.",
        'delay': "Postpone reminder for:",
        'tmrw': "tomorrow",
        'del': "Reminder has been deleted.",
        'error_2': "You have no active reminders.",
        'delay_by': "Reminder delayed by",
        'new_time': "New time:",
        'time': "Date and time:",
        'task': "Task:",
        'del_r': "Delete reminder"
    },
    'Čeština': {
        'set_language': "Jazyk je nastaven na",
        'language_set': "Jazyk už je nastaven na",
        'change_lang': "Jazyk je změněno na",
        'location_set': "Vaše poloha je nastavena na",
        'change_tz': "Vaše poloha je změněna na",
        'no_change_tz': "Vaše poloha už je nastavena na",
        'cur_time': "Aktuální čas ve vašem časovém pásmu:\n",
        'invalid_tz': "Vaše poloha je neplatná. Zkuste to znovu.",
        'not_set': "Nejprve nastavte svoji polohu.",
        'reminder_set': "Připomínka je nastavena na",
        'reminder_today': "Připomínka je nastavena na dnešek na",
        'reminder_tomorrow': "Připomínka je nastavena na zítra na",
        'choose_time': "Prosím, vyberte čas pro připomínku.",
        'reminder': "Připomínka:",
        'error': "Chyba: připomínka je nastavena na minulý čas.",
        'delay': "Odložit připomenutí o:",
        'tmrw': "zítra",
        'del': "Připomínka je smazána.",
        'error_2': "Nemáte žádná aktivní připomenutí.",
        'delay_by': "Připomenutí odloženo o",
        'new_time': "Nový čas:",
        'time': "Datum a čas:",
        'task': "Úkol:",
        'del_r': "Smazat připomínku"
    }
}

hlp = {'Čeština': """
- Pro nastavení připomínky na dnešek napište:
  `/reminder Úkol Čas`
  Příklad: `/reminder Jóga 18:00`

- Pro nastavení připomínky na zítra použijte:
  `/reminder Úkol zítra Čas`
  Příklad: `/reminder Matematika zítra 12:00`

- Pro nastavení připomínky na konkrétní datum napište:
  `/reminder Úkol Čas Datum`
  Příklad: `/reminder Zasedání 09:00 24.08.2024`

Další užitečné příkazy:

/list - zobrazit všechny aktivní připomínky;
/change_lang - změnit jazyk bota;
/change_tz - změnit časové pásmo (pošlete zprávu ve formátu `/change_tz Continent/City`).
""",
       'English': """
- To set a reminder for today, use:
  `/reminder Task Time`
  Example: `/reminder Math homework 22:00`

- To set a reminder for tomorrow, use:
  `/reminder Task tomorrow Time`
  Example: `/reminder Meeting tomorrow 12:00`

- To set a reminder for a specific date, use:
  `/reminder Task Time Date`
  Example: `/reminder Swimming pool 09:00 24.08.2024`

Other useful commands: 

/list - to view all your active reminders; 
/change_lang - to change bot language;
/change_tz - to change your timezone (send message in a format `/change_tz Continent/City`).
"""}
