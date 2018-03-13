#!/usr/bin/python3
# coding utf-8
import subprocess
out_butes = subprocess.check_output(['netstat', '-a']).decode('utf-8')
print(out_butes)

"""
if the executed command returns a nonzero exit code, an exception is raised. Here is an example of catching errors and 
getting the output created along with the exit code
"""
try:
    out_bytes = subprocess.check_output(['cmd', 'arg1', 'arg2'])
except subprocess.CalledProcessError as e:
    out_bytes = e.output       # Output generated before error
    code = e.returncode  # Return code


# 默认情况下,check_output 命令只会捕获命令的标准输出.如果想捕获命令的错误输出,需要将错误输出重定向到标准输出
output = subprocess.check_output(['cmd', 'arg1', 'arg2'], stderr=subprocess.STDOUT)

"""
subprocess 提供的便利函数都是对 Popen 类的封装,当便利函数无法满足业务的需求时,也可以使用Popen类.

subprocess.Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, 
                 close_fds=<object object at 0x7fddee5be100>, shell=False, cwd=None, env=None, 
                 universal_newlines=False, startupinfo=None, creationflags=0,  
                 restore_signals=True, start_new_session=False, pass_fds=())

在 Unix 系统中,当 shell 设置为 True 时, shell 默认使用 /bin/sh. args 是需要执行的命令, 可以是一个命令字符串,也可以是一个字符串列表
Popen 对象创建后,子进程便会运行.Popen 提供了若干方法来控制子进程的运行:
    wait: 等待子进程结束
    poll: 检查子进程状态
    kill: 给子进程发送 SIGKILL 信号终止子进程
    terminal: 给子进程发送 SIGTERM 信号终止子进程
    communicate: 与子进程进行交互
"""
def execute_cmd(cmd):
    """
    使用 Popen 封装一个执行 shell 命令的函数
    :param cmd:
    :return:
    """
    p = subprocess.Popen(cmd,
                         shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    #
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        return p.returncode, stderr
    return p.returncode, stdout
