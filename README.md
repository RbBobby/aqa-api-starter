# AQA API Starter

Учебный минимум API-автотестов для [Automation Exercise](https://automationexercise.com/api_list).

Это **скелет для обучения**, не полный фреймворк. UI-тестов здесь нет специально: сначала Client → Service → Test, потом Git/GitHub, потом расширение.

Полный проект-образец (API + Selenium UI + login/user lifecycle): [`autotests_automationexercise`](https://github.com/RbBobby/autotests_automationexercise).

| Набор | Технологии | Паттерн | Запуск |
|-------|------------|---------|--------|
| **API** (2 теста) | pytest, requests | API Client + Service Object, AAA | `pytest -v` — браузер не нужен |

Тесты ходят на **живой** сайт `automationexercise.com` — нужен интернет.

---

## Быстрый старт

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt   # Ruff (опционально)

pytest -v
```

Опционально переопределить URL:

```bash
cp .env.example .env
# при необходимости измените API_BASE_URL / API_TIMEOUT
```

---

## Как устроен проект

```text
test  →  ProductsService.get_products()  →  ApiClient.get()  →  automationexercise.com/api
         ↑ fixture (DI)
         ↑ response.body (ApiBody dataclass)
```

- **ApiClient** — единственная точка HTTP (`requests.Session`).
- **Service** — один класс на эндпоинт, тест не знает URL.
- **Fixture** — pytest сам собирает `settings → api_client → products_service`.
- **AAA** — Arrange в fixture, в тесте Act + Assert.

> Сайт часто отвечает **HTTP 200** при ошибке. Смотрите `response.body.response_code`, не только `status_code`. Это проверяет `test_post_products_returns_405`.

```text
aqa-api-starter/
├── api/
│   ├── client/api_client.py      # ApiClient, ApiResponse
│   ├── config/settings.py        # .env → Settings
│   ├── models/responses.py       # Product, Brand, ApiBody
│   └── services/
│       ├── products_service.py   # GET/POST /productsList
│       └── brands_service.py     # GET/PUT /brandsList (тесты — ваша практика)
├── tests/api/
│   ├── conftest.py               # fixtures
│   └── test_products_list.py     # 2 теста — учебный минимум
├── docs/git-github-lecture.md    # лекция + практикум Git / GitHub
├── .github/workflows/tests.yml   # CI: lint → api-tests
├── pytest.ini
└── requirements.txt
```

---

## Git и GitHub

Практикум: [`docs/git-github-lecture.md`](docs/git-github-lecture.md).

Remote на GitHub **специально не подключён** — это часть лекции. Первый локальный коммит уже есть; дальше вы создаёте репозиторий, `git remote add`, push и PR сами.

---

## Что добавить дальше

Не реализуйте всё сразу. Один шаг — одна ветка — один PR (см. лекцию).

- [ ] Тесты на `BrandsService` (сервис уже есть) — GET 200 и PUT 405
- [ ] `SearchService` + POST `/searchProduct` (с параметром и без)
- [ ] `@pytest.mark.parametrize` для нескольких поисковых запросов
- [ ] Более строгие модели / jsonschema на ответ
- [ ] Allure или другой отчёт кроме pytest-html
- [ ] Playwright UI — **отдельный следующий репозиторий**, не этот

---

## Линтер

```bash
pip install -r requirements-dev.txt
ruff check .
ruff format .
```

В CI job **Lint (Ruff)** идёт перед API-тестами.

---

## HTML-отчёт

```bash
mkdir -p reports
pytest -v --html=reports/api-report.html --self-contained-html
```

Папка `reports/` в `.gitignore`.

---

## CI (GitHub Actions)

После того как вы запушите репозиторий (практика из лекции), workflow [`.github/workflows/tests.yml`](.github/workflows/tests.yml):

| Job | Команда |
|-----|---------|
| `lint` | `ruff check` + `ruff format --check` |
| `api-tests` | `pytest -m api` (после успешного lint) |

Badge (подставьте свой логин и имя репо):

```markdown
![Tests](https://github.com/<логин>/<репозиторий>/actions/workflows/tests.yml/badge.svg)
```
