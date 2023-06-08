# Бот по сбору анкет пользователей Telegram-канала Peredelano Startups

[Данный бот](https://t.me/Peredelano_bot) - это первое с чем взаимодействуют новые пользователи, которые хотят попасть в Peredelano Startups. Бот занимается тем, что собирает первичные данные, такие как:
- Роль пользователя (Backend, Frontend и т.д.)
- Технологический стек
- Опыт

В дальнейшем планируется расширить анкету еще несколькими пунктами и дать возможность пользователям полноценно изменять свои данные (сейчас это можно сделать только пройдя всего бота заново, тогда все данные обновятся)

Конечной целью данного бота является автоматический подбор команды для новых пользователей, а также предоставление пользователю краткого роадмапа по итогам заполнения анкеты. Ну и важные сообщения он будет иногда получать🤗

## Development

This section contains general and trivially information for those who intend to make changes to the project code.

### Requirements

- git
- docker
- docker compose

### Local environment

Clone code to your workstation.

```bash
#!/bin/bash
git clone git@github.com:openworld-community/peredelano_entry_bot.git
```

Create new branch for you code with new feature/fix/refactoring.

```bash
#!/bin/bash
git checkout -b <MyNewBranch>
```

Make sure that the local ".env" environment variable file contains all the necessary data. If necessary, make your own changes.

```bash
#!/bin/bash
cat .env
```

Pull latest docker image.

```bash
#!/bin/bash
docker compose pull
```

**Notice**: To override the behavior of "docker-compose.yml" when developing locally, use the "docker-compose.override.yml" file.

In other way you can build image locally. Change value of variable 'TAG' an '.env' file before build local image.

```bash
#!/bin/bash
cat .env |grep -i tag
TAG=local
```

Run the application.

```bash
#!/bin/bash
docker compose up -d
```

Stop the application.

```bash
#!/bin/bash
docker compose down --remove-orphans
```

Use a local code quality check with [local pre-commit hook with linter](./.githooks/README.md). By doing this, you will help our community
reduce the **[cost of GitHub infrastructure](https://docs.github.com/ru/billing/managing-billing-for-github-actions/about-billing-for-github-actions)**.

