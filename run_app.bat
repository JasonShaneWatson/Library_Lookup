start cmd /k python3 lib_app_librarian.py
start cmd /k python3 lib_app_bookSrv.py
start cmd /k python3 lib_app_userSrv.py
timeout /t 3 /nobreak
start cmd /K "echo Running: python3 lib_app_client.py 'input.json' & python3 lib_app_client.py input.json"

