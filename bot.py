Running 'python bot.py'
INFO:tg-bot:Starting webhook on port 10000
INFO:httpx:HTTP Request: POST https://api.telegram.org/bot8254016879:AAG357kGbNnw3RoAeF7Z8M6_UqBr0fBi-7A/getMe "HTTP/1.1 200 OK"
Traceback (most recent call last):
  File "/opt/render/project/src/bot.py", line 52, in <module>
    main()
  File "/opt/render/project/src/bot.py", line 44, in main
    app.run_webhook(
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telegram/ext/_application.py", line 910, in run_webhook
    return self.__run(
           ^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telegram/ext/_application.py", line 967, in __run
    raise exc
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telegram/ext/_application.py", line 959, in __run
    loop.run_until_complete(updater_coroutine)  # one of updater.start_webhook/polling
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/python/Python-3.11.11/lib/python3.11/asyncio/base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telegram/ext/_updater.py", line 498, in start_webhook
    raise RuntimeError(
RuntimeError: To use `start_webhook`, PTB must be installed via `pip install "python-telegram-bot[webhooks]"`.
     ==> Deploying...
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telegram/ext/_updater.py", line 498, in start_webhook
    raise RuntimeError(
RuntimeError: To use `start_webhook`, PTB must be installed via `pip install "python-telegram-bot[webhooks]"`.
     ==> Exited with status 1
     ==> Common ways to troubleshoot your deploy: https://render.com/docs/troubleshooting-deploys
==> Running 'python bot.py'
INFO:tg-bot:Starting webhook on https://lerus-bot.onrender.com/8254016879:AAG357kGbNnw3RoAeF7Z8M6_UqBr0fBi-7A
INFO:httpx:HTTP Request: POST https://api.telegram.org/bot8254016879:AAG357kGbNnw3RoAeF7Z8M6_UqBr0fBi-7A/getMe "HTTP/1.1 200 OK"
Traceback (most recent call last):
  File "/opt/render/project/src/bot.py", line 84, in <module>
    main()
  File "/opt/render/project/src/bot.py", line 75, in main
    app.run_webhook(
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telegram/ext/_application.py", line 910, in run_webhook
    return self.__run(
           ^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telegram/ext/_application.py", line 967, in __run
    raise exc
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telegram/ext/_application.py", line 959, in __run
    loop.run_until_complete(updater_coroutine)  # one of updater.start_webhook/polling
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/python/Python-3.11.11/lib/python3.11/asyncio/base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telegram/ext/_updater.py", line 498, in start_webhook
    raise RuntimeError(
RuntimeError: To use `start_webhook`, PTB must be installed via `pip install "python-telegram-bot[webhooks]"`.
