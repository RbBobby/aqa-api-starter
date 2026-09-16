# Git и GitHub для AQA: лекция и практикум

Аудитория: человек, который идёт в Junior Automation QA. Git почти с нуля.  
Площадка: этот репозиторий `aqa-api-starter`.

Цель занятия: не выучить все флаги git, а **уверенно жить в ветках, коммитах и PR** так, как это делают в команде автотестов.

Правило на всю лекцию: команды ниже выполняйте **из корня** `aqa-api-starter`, не из соседнего полного проекта.

---

## Содержание

1. [Зачем Git тестировщику](#часть-1-зачем-git-тестировщику)
2. [Локальный Git](#часть-2-локальный-git)
3. [Практика 1 — ветка и коммит](#практика-1-ветка-и-коммит-на-этом-репо)
4. [GitHub](#часть-3-github)
5. [Практика 2 — remote, push, PR, CI](#практика-2-remote-push-pr-ci)
6. [Конфликты и ритм AQA](#часть-4-конфликты-и-ежедневный-ритм-aqa)
7. [Практика 3 — учебный конфликт](#практика-3-учебный-конфликт)
8. [Шпаргалка](#часть-5-мини-шпаргалка)
9. [Чеклист «я умею»](#чеклист-я-умею)

---

## Часть 1. Зачем Git тестировщику

Автотесты — такой же код, как продукт. Их хранят в git, ревьюят в Pull Request, гоняют в CI на каждый push.

Без git вы можете запустить `pytest` локально. С git вы можете:

- показать **diff** («вот что я изменил в `ProductsService`»);
- откатиться, если новый тест сломал старый;
- работать параллельно: коллега пишет поиск, вы пишете brands — в разных ветках;
- получить **зелёный pipeline** на GitHub, а не скриншот терминала.

### Словарь на одну минуту

| Термин | Простыми словами |
|--------|------------------|
| **Репозиторий** | Папка проекта + скрытая история в `.git` |
| **Коммит** | Снимок изменений с сообщением «зачем» |
| **Ветка** | Параллельная линия истории (`main` — стабильная, `feature/...` — ваша задача) |
| **Remote** | Копия на сервере (GitHub). Локальный git про неё не знает, пока не добавите `origin` |
| **PR (Pull Request)** | Запрос «влить мою ветку в `main`» + обсуждение + CI |

Этот starter уже локальный git-репозиторий. **Remote специально не подключён** — вы добавите его в практике 2.

---

## Часть 2. Локальный Git

### Состояние: что уже есть

Проверьте:

```bash
git status
git log --oneline -5
```

Ожидание:

- ветка `main`;
- рабочая копия чистая (`nothing to commit, working tree clean`);
- есть как минимум один коммит со стартовым каркасом.

Если `git status` пишет `not a git repository` — вы не в той папке.

### `status` / `diff` / `log`

| Команда | Зачем |
|---------|--------|
| `git status` | Что изменено, что ещё не в индексе |
| `git diff` | Непроиндексированный diff |
| `git diff --staged` | То, что пойдёт в следующий коммит |
| `git log --oneline` | Краткая история |

Привычка AQA: **перед коммитом** смотреть `status` и `diff`. Так вы не закоммитите `.env` или случайный `report.html`.

### `.gitignore`

Файл `.gitignore` говорит git: «эти пути не версионировать».

В этом проекте игнорируются:

- `.venv/` — виртуальное окружение (на каждой машине своё);
- `.env` — настройки и будущие секреты;
- `reports/` — HTML-отчёты pytest;
- `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`.

`.env.example` **не** в ignore — это шаблон без секретов, его коммитят.

### Индекс и коммит

```bash
git add путь/к/файлу          # положить в индекс (staging)
git commit -m "сообщение"
```

Не делайте `git add .` вслепую, пока не освоитесь: сначала `git status`.

**Хорошее сообщение — про «зачем», не про «что».**

| Плохо | Лучше |
|-------|--------|
| `update` | `Add GET /brandsList assertions so catalog is not empty` |
| `fix tests` | `Assert responseCode 405 on POST /productsList` |
| `asdf` | (не коммитить) |

Для этого репо достаточно одного-двух предложений на английском или русском — главное, чтобы по `git log` было понятно, **какую проверку вы добавили**.

### Ветки

`main` — договорённость: сюда попадает только проверенное.

Рабочий ритм:

```bash
git checkout main
git checkout -b feature/brands-tests
```

Имя ветки = задача. Примеры для этого starter:

- `feature/brands-tests`
- `feature/search-product`
- `docs/readme-run-tips`

Не коммитьте учебные эксперименты сразу в `main`: так сложнее открыть PR и проще потерять стабильный каркас.

Вернуться на main:

```bash
git checkout main
```

Посмотреть ветки:

```bash
git branch
```

### `stash` — коротко

Нужно срочно переключить ветку, а правки ещё сырые:

```bash
git stash push -m "wip search service"
git checkout main
# ... потом
git checkout feature/search-product
git stash pop
```

Не используйте stash как замену коммиту: это временный карман, его легко забыть.

---

## Практика 1. Ветка и коммит на этом репо

Цель: пройти цикл «ветка → правка → коммит», не трогая GitHub.

`BrandsService` уже есть, тестов на него нет — это ваша первая задача.

1. Убедитесь, что вы на `main` и дерево чистое:

   ```bash
   git checkout main
   git status
   ```

2. Создайте ветку:

   ```bash
   git checkout -b feature/brands-tests
   ```

3. Создайте файл `tests/api/test_brands_list.py` **по образцу** `tests/api/test_products_list.py`:
   - GET `/brandsList` → HTTP 200, `body.response_code == 200`, список брендов не пустой;
   - PUT `/brandsList` → HTTP 200, `body.response_code == 405`.
   - Fixture `brands_service` уже описана в `tests/api/conftest.py`.

4. Запустите:

   ```bash
   pytest tests/api/test_brands_list.py -v
   pytest -v
   ```

   Должны пройти и старые 2 теста products, и новые brands.

5. Посмотрите, что git видит:

   ```bash
   git status
   git diff
   ```

6. Добавьте только тест (не `.venv`, не отчёты):

   ```bash
   git add tests/api/test_brands_list.py
   git commit -m "$(cat <<'EOF'
   Add brandsList API tests for GET 200 and PUT 405.

   EOF
   )"
   ```

7. Проверьте историю:

   ```bash
   git log --oneline -5
   git show --stat
   ```

На этом практика 1 закончена. Ветку пока **не удаляйте** — она понадобится в практике 2. Если хотите отложить push: можно сразу перейти к части 3 и вернуться к этой ветке позже.

---

## Часть 3. GitHub

Git — программа на вашем компьютере. GitHub — хостинг репозиториев + PR + Actions.

Для Junior AQA GitHub — это портфолио: рекрутер смотрит README, структуру, зелёный CI, осмысленные PR.

### Создать пустой remote

На github.com:

1. **New repository**.
2. Имя, например `aqa-api-starter`.
3. **Без** README, `.gitignore` и лицензии — они уже есть локально. Иначе GitHub создаст чужой первый коммит, и первый `push` усложнится.
4. Репозиторий может быть public (удобно для портфолио).

Скопируйте URL вида `https://github.com/<логин>/aqa-api-starter.git`.

### Подключить remote

```bash
git remote add origin https://github.com/<логин>/aqa-api-starter.git
git remote -v
```

`origin` — обычное имя «того сервера». Один локальный репо — один `origin` на старте.

### Первый push `main`

```bash
git checkout main
git push -u origin main
```

`-u` запоминает, что локальный `main` связан с `origin/main`. Дальше достаточно `git push` / `git pull`.

После push откройте репозиторий в браузере: должен быть тот же README, что локально.

### README и badge CI

После первого успешного прогона Actions можно вставить badge (подставьте логин и имя репо):

```markdown
![Tests](https://github.com/<логин>/aqa-api-starter/actions/workflows/tests.yml/badge.svg)
```

Это делается отдельным маленьким PR — хороший тон, не смешивать badge и новый сервис в одном diff.

### Issues vs Pull Request

| | Issue | Pull Request |
|--|--------|----------------|
| Это | Задача / баг / идея | Предложение влить код |
| Код | Не обязателен | Ветка с коммитами |
| Пример | «Добавить SearchService» | PR с файлами сервиса и теста |

Новичку достаточно PR. Issue полезны, когда задач много и вы хотите трекать очередь.

### Как открыть PR

1. Запушить feature-ветку (`git push -u origin feature/brands-tests`).
2. На GitHub: **Compare & pull request**.
3. Title — как хорошее commit message.
4. Description: что проверили, как запустить (`pytest tests/api/test_brands_list.py -v`).
5. Base: `main`, compare: ваша ветка.
6. Дождаться CI. Если красный — чините в той же ветке, новый `git push` (без force).
7. Merge. Для учёбы достаточно **Create a merge commit** или **Squash**.

Ревьюер на работе смотрит: размер diff, понятность тестов, нет ли секретов, зелёный pipeline.

### GitHub Actions в этом проекте

Файл: [`.github/workflows/tests.yml`](../.github/workflows/tests.yml).

Что происходит:

```text
push или pull_request в main
        │
        ▼
   Job lint (Ruff)
        │ успех
        ▼
   Job api-tests (pytest -m api)
        │
        ▼
   artifact: api-report.html
```

Триггеры: `push`, `pull_request`, ручной `workflow_dispatch`.

Зачем lint перед тестами: сломанный импорт и грязный стиль дешевле поймать за секунды, чем гонять HTTP к живому сайту.

Где смотреть: вкладка **Actions**. Артефакт HTML-отчёта скачивается с прогона, даже если тесты упали (`if: always()`).

### Secrets: почему пароли не в git

В учебном минимуме login-тестов нет. На полном проекте (`autotests_automationexercise`) для verify-login нужны `TEST_USER_EMAIL` / `TEST_USER_PASSWORD`.

Правило, которое стоит запомнить сейчас:

- `.env` — локально, в git не попадает (см. `.gitignore`);
- в CI те же значения кладут в **Settings → Secrets and variables → Actions**;
- в workflow их читают как `${{ secrets.NAME }}`, не как текст в YAML.

Если пароль один раз попал в коммит, мало удалить его из файла: он остаётся в истории. Для учёбы не коммитьте `.env` вообще. `git reset --hard` историю уже опубликованного секрета не лечит — только ротация пароля.

---

## Практика 2. Remote, push, PR, CI

Делайте по порядку. Если практика 1 ещё не сделана — сначала она.

1. Создайте пустой репозиторий на GitHub (без README).

2. На `main` добавьте remote и запушьте каркас:

   ```bash
   git checkout main
   git remote add origin https://github.com/<логин>/aqa-api-starter.git
   git push -u origin main
   ```

3. Запушьте ветку с тестами brands:

   ```bash
   git checkout feature/brands-tests
   git push -u origin feature/brands-tests
   ```

4. Откройте Pull Request в `main`. В описании укажите:
   - какие эндпоинты покрыты;
   - команду прогона;
   - что HTTP 200 ≠ успех, смотрим `responseCode`.

5. Вкладка **Actions**: дождитесь зелёных `lint` и `api-tests`.

6. Merge PR. Локально подтяните `main`:

   ```bash
   git checkout main
   git pull
   ```

7. Ветка `feature/brands-tests` после merge больше не нужна:

   ```bash
   git branch -d feature/brands-tests
   git push origin --delete feature/brands-tests
   ```

   Удаление remote-ветки — нормально; история остаётся в merge-коммите.

---

## Часть 4. Конфликты и ежедневный ритм AQA

### `pull` vs `pull --rebase`

```bash
git pull              # fetch + merge (часто появляется merge-коммит)
git pull --rebase     # fetch + поставить ваши коммиты поверх свежего main
```

На работе чаще просят rebase feature-ветки на актуальный `main`, чтобы PR был линейнее:

```bash
git checkout feature/search-product
git fetch origin
git rebase origin/main
```

Если rebase страшно — `git pull` тоже рабочий вариант для учёбы. Главное: **перед новым PR подтянуть `main`**, иначе вы ревьюите чужой устаревший код.

### Конфликт

Git останавливается, в файле появляются маркеры:

```text
<<<<<<< HEAD
текст из текущей ветки
=======
текст из вливаемой ветки
>>>>>>> feature/other
```

Что делать:

1. Открыть файл, понять **оба** изменения.
2. Собрать итоговый текст, **удалить** все `<<<<<<<`, `=======`, `>>>>>>>`.
3. Не выкидывать чужой абзац только потому, что он мешает.
4. `git add` файл, затем:
   - при merge: `git commit`;
   - при rebase: `git rebase --continue`.

Отменить незавершённый rebase: `git rebase --abort`.

### `revert` vs паника с reset

| Приём | Когда |
|--------|--------|
| `git revert <commit>` | Коммит уже в `main` / на remote: сделать новый коммит, который отменяет старый |
| `git restore файл` | Локально испортили файл, коммита ещё нет |
| `git reset --hard` | Стирает незакоммиченное **навсегда**. Не рабочий приём «на каждый день» |

**Force push (`git push --force`) в `main` — никогда.** Даже в свою feature-ветку force имеет смысл только если вы один на ветке и понимаете, что переписываете историю.

### Ритм, который ждут на Junior+

- одна задача = одна ветка = один PR;
- маленький diff проще ревьюить, чем «я за неделю переписал всё»;
- не смешивать рефакторинг клиента и новый тест поиска в одном PR;
- CI должен быть зелёным до merge.

Для этого starter следующий PR после brands — логично `SearchService`, а не сразу jsonschema + Allure + Playwright.

---

## Практика 3. Учебный конфликт

Цель: один раз увидеть конфликт в безопасной среде, а не на рабочем `main`.

Сценарий: две ветки правят **один и тот же абзац** `README.md`.

1. Обновите `main` и убедитесь, что он чистый:

   ```bash
   git checkout main
   git pull   # если origin уже есть; иначе пропустите
   ```

2. Ветка A — добавьте в конец README строку про запуск brands:

   ```bash
   git checkout -b experiment/readme-a
   ```

   Допишите, например: `pytest tests/api/test_brands_list.py -v`.  
   Закоммитьте: `Document how to run brands tests`.

3. Вернитесь на `main` (без merge A) и создайте ветку B:

   ```bash
   git checkout main
   git checkout -b experiment/readme-b
   ```

   В **том же месте** README напишите другую фразу, например про HTML-отчёт.  
   Закоммитьте: `Document html report command`.

4. Влейте A в B и получите конфликт:

   ```bash
   git checkout experiment/readme-b
   git merge experiment/readme-a
   ```

5. Откройте `README.md`, оставьте **обе** полезные мысли одним связным текстом, уберите маркеры конфликта.

6. Завершите merge:

   ```bash
   git add README.md
   git commit -m "Merge readme experiments and keep both run tips"
   ```

7. Учебные ветки можно удалить, в `main` это merge не обязательно тащить:

   ```bash
   git checkout main
   git branch -D experiment/readme-a experiment/readme-b
   ```

   `-D` — удалить, даже если не сливали в `main`. Для эксперимента это нормально.

Если GitHub уже подключён, **не пушьте** `experiment/*` — это только локальный тренажёр.

---

## Часть 5. Мини-шпаргалка

| Команда | Когда использовать | Типичная ошибка |
|---------|-------------------|-----------------|
| `git status` | Перед add/commit/checkout | Не смотреть и коммитить лишнее |
| `git diff` / `git diff --staged` | Перед коммитом | Сообщение «fix», а в diff половина рефакторинга |
| `git add <файл>` | Индексировать осознанно | `git add .` вместе с `.env` и `reports/` |
| `git commit -m "..."` | Зафиксировать логичный кусок | Пустые или бессмысленные сообщения |
| `git checkout -b feature/...` | Новая задача | Коммиты сразу в `main` |
| `git log --oneline` | Понять историю | Не смотреть, откуда выросла ветка |
| `git stash` | Срочно сменить ветку | Забыть `stash pop` и потерять правки «в голове» |
| `git remote add origin <url>` | Один раз на репо | Добавить origin дважды / не тот URL |
| `git push -u origin <ветка>` | Отправить ветку на GitHub | Force push «чтобы прошёл» |
| `git pull` / `git pull --rebase` | Подтянуть `main` перед PR | Пушить неделю без rebase и ловить огромный конфликт |
| `git merge` | Слить ветки | Оставить маркеры `<<<<<<<` в файле |
| `git revert` | Отменить уже опубликованное | `reset --hard` по уже запушенному `main` |
| `git restore <файл>` | Откатить локальный файл | Путать с удалением с диска вне git |

---

## Чеклист «я умею»

Отметьте, когда сделали руками, а не только прочитали.

- [ ] `git status`, `git diff`, `git log` — понятно, что показывает каждая
- [ ] Знаю, зачем `.gitignore` и почему `.env` не в репозитории
- [ ] Создаю ветку `feature/...`, а не коммичу учёбу в `main`
- [ ] Пишу commit message про смысл проверки, не «update»
- [ ] Сделал практику 1: тесты на `BrandsService` + коммит
- [ ] Создал пустой GitHub-репо, добавил `origin`, запушил `main`
- [ ] Открыл PR, дождался зелёного Actions, сделал merge
- [ ] Могу объяснить, что делают jobs `lint` и `api-tests`
- [ ] Один раз сам разрешил конфликт (практика 3)
- [ ] Понимаю: `revert` для опубликованного, force push в `main` — никогда
- [ ] Следующую фичу (поиск / parametrize) планирую как отдельный PR

Дальше по коду — раздел [«Что добавить дальше»](../README.md#что-добавить-дальше) в README.
