RU_USER_HANDLERS: dict[str, str] = {
    'command_start': 'Привет! Ты зашел в Peredelano Startups.\n\nПеред тем как получить ссылку на наш канал в'
                     ' Telegram, тебе необходимо создать профиль, чтобы мы могли определить '
                     'тебя в соответствующую группу. '
                     'Готов?\n\nДля отмены заполнения анкеты используй /cancel',
    'get_specialization': 'Выбери роль (кем ты себя видишь в команде).\n\nЕсли твоей роли нет среди '
                          'представленных, просто напиши её в этом сообщении.\n\n'
                          'Если ты умеешь делать сразу несколько вещей, то выбери самую '
                          'приоритетную для тебя или также напиши это в сообщении.',
    'check_experience': 'Есть ли у тебя коммерческий опыт?\n\nПод коммерческим опытом мы имеем в виду '
                        'опыт работы в компании над продуктом, который приносит этой компании деньги',
    'choose_tech_stack': 'Перечисли через запятую стек технологий или знания, которыми обладаешь.\n\n'
                         'Например: Pandas, Kubernetes, Git, FastAPI',
    'provide_linkedin_link': 'Добавь ссылку на свой LinkedIn профайл. Это поможет нам связать тебя с '
                             'коллегами и единомышленниками из нашего сообщества.\n\nЭто поле не является обязательным к '
                             'заполнению, поэтому если по каким-то причинам ты не хочешь давать ссылку на свой профайл, '
                             'то просто нажми "Пропустить".\n\nФормат ссылки на профиль:\n'
                             '<code>https://www.linkedin.com/in/vasia-pupkin-71b9b76b/</code>',
    'wrong_linkedin_link': 'Боюсь, что это не является верным форматом ссылки (как в примере выше). Пожалуйста, введи ссылку '
                           'правильного формата или нажми на кнопку "Пропустить"',
    'summary': 'Проверь все еще раз и если все правильно, подтверди.\n\nЕсли что-то не так, просто пройди '
               'анкету сначала и данные обновятся.\n\n',
}

RU_USER_HANDLERS_BUTTONS: dict[str, list[str]] = {
    'roles': ["Backend", "Frontend", "Mobile", "DevOps", "QA", "Marketing", "PM", "PO", "CTO", "CEO", "CPO",
              "UI Designer", "UX Designer", "ML", "Contentmaker", "TechLead", "HR", "GameDev", "Graphic Designer",
              "Data Analytic"],
    'choose_experience': ["До года", "1-3 года", "3-5 лет", "Свыше 5 лет", "Не работаю"],
    'skip_linkedin': ["Пропустить"],
    'finalize_profile': ["Подтвердить", "Отмена"],
}

RU_ADMIN_HANDLERS: dict[str, str] = {
    'hello_admin': 'Поздравляю! Ты - администратор бота 🤗\n\nНиже представлено меню администратора (иногда нижнее '
                   'меню сворачивается, можно развернуть его кнопкой вроде этой: 🎛)',
    'write_mailing_message': 'Напиши сообщение, которое нужно отправить пользователям ⤵',
    'choose_mailing_list_type': 'Кому рассылать будем?\n\nРассылка адресована тем кто:',
    'summary': 'Проверь данные и если все правильно, нажми "Начать рассылку". Если что-то неверно, нажми "Отмена" '
               'и начни заново.\n\n',
    'mailing_has_started': 'Отлично! Рассылка успешно начата! 🫡\n\nМожете начать новую по команде /admin '
                           'или заняться чем-либо еще.'
}

RU_OTHER_HANDLERS: dict[str, str] = {
    'cancel_handler': 'Действие отменено. Вы можете начать заново, набрав /start',
}

RU_MISC_HANDLERS: dict[str, str] = {
    'wrong_answer': 'К сожалению, я не настолько умен, чтобы ответить на твое сообщение :( '
                    '\nНажми на кнопку для продолжения (иногда нижнее меню сворачивается, '
                    'можно развернуть его кнопкой вроде этой: 🎛) или набери /cancel для '
                    'того, чтобы начать заново',
}
