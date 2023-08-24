@echo off
if "s"%1 == "s"  goto noparam

D:\home\projects\pymemorium\alembic.cmd revision --message=%1 --autogenerate
goto exit

:noparam
D:\home\projects\pymemorium\alembic.cmd revision --message="No message" --autogenerate
:exit