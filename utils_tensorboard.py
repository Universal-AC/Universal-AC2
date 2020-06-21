from tensorboard import notebook
import os
import datetime
import shlex

def kill_all_tensorboard():
    """
    détruit tous les serveurs tensorboard
    """
    import tempfile
    path = os.path.join(tempfile.gettempdir(), ".tensorboard-info")
    for i in os.listdir(path) :
        os.unlink(path+'\\'+i)
    os.system("taskkill /F /IM tensorboard.exe")
    
def kill_pid_tensorboard(pid):
    """
    détruit le tensorboards correspondant au pid
    """
    
    import tempfile
    try:
        path = os.path.join(tempfile.gettempdir(), ".tensorboard-info")
        os.unlink(path+'\\pid-'+str(pid)+".info")
    except:
        print("Fichier introuvable")
    os.system("taskkill /F /PID "+str(pid))
    
def kill_port_tensorboard(port):
    """
    détruit les tensorboards utilisant le port indiqué
    """
    occupied = port_occupied(port)
    for i in port_occupied(port):
        print("port {} occupé, kill pid {}".format(port, i.pid))
        kill_pid_tensorboard(i.pid)
    
def port_occupied(port):
    """
    Retourne les tensorboard qui utilise le port indiqué
    """
    l = []
    for i in notebook.manager.get_all():
        if i.port == port:
            l += [i]
    return l

def launch_tensorboard(log_file, port = 6006):
    """
    Contruit un serveur tensorboard au port indiqué à partir de log_file.
    Si le port est déjà pris, détruit les anciens serveurs 
    """
    kill_port_tensorboard(port)
    parsed_args = shlex.split("--logdir {} --port {}".format(log_file,port), comments=True, posix=True)
    start_result = notebook.manager.start(parsed_args, timeout=datetime.timedelta(seconds=10))
    notebook.display(port)
    
def affiche_port(port):
    """
    affiche le tensorboard du port indiqué
    """
    notebook.display(port)
    
def affiche_all_tensorboard():
    """
    affiche les serveurs tensorboard actifs
    """
    l = notebook.manager.get_all()
    for i in l:
        print("pid : {} | port : {} | logdir : {}".format(i.pid, i.port, i.logdir))

