#!/usr/bin/env python3

class File:
    type_file = '-' 
    read_ow = 'r'
    write_ow = 'w'
    execute_ow = '-'

    read_ot = 'r'
    write_ot = '-'
    execute_ot = '-'

    def __init__(self,name):
        self.name = name

    def get_type(self):return self.type_file
    def set_type(self,type_file):self.type_file = type_file

    def get_row(self):return self.read_ow
    def get_wow(self):return self.write_ow
    def get_xow(self):return self.execute_ow
    
    def get_rot(self):return self.read_ot
    def get_wot(self):return self.write_ot
    def get_xot(self):return self.execute_ot

    def get_name(self): return self.name

    def set_read(self,read): self.read = read
    def set_write(self,write): self.write = write
    def set_execute(self,execute): self.execute = execute
    def set_name(self,name): self.name = name

    def __repr__(self):
        return str(self.name)

class Folder(File):
    type_file = 'd' 
    read_ow = 'r'
    write_ow = 'w'
    execute_ow = 'x'

    read_ot = 'r'
    write_ot = '-'
    execute_ot = 'x'


class User:
    def __init__(self,name = 'root'):
        self.name = name
    
    def get_name(self):return self.name

    def __repr__(self):
        return str(self.name)


class Terminal:

    def __init__(self):
        self.root_user = User('root') 
        self.users = []
        self.users.append(self.root_user)
        print(self.users)

        #Creating root folder
        self.root = {}
        self.root_folder = Folder('/')
        self.root[self.root_folder] = {}
        self.root_bin = self.root

        object_keys = list(self.root.keys())
        self.root = self.root[object_keys[0]]

        # When the program starts
        self.cur_dir = self.root
        self.cur_path = '/'
        self.cur_terminaluser = self.root_user
        while True:
            #Display the terminal
            promt = self.cur_terminaluser.get_name() + ':' + self.cur_path + '$ '
            # Receive comman string
            command = input(str(promt))
            command = command.split()

            # Commands 
            if command[0] == 'mkdir':
                self.mkdir_command(command,self.cur_dir)

            elif command[0] == 'touch':
                self.touch_command(command,self.cur_dir)
            
            elif command[0] == 'cd':
                self.cd_command(command, self.cur_dir, self.cur_path)
                if len(self.cur_path) > 1 :
                    if self.cur_path[0] == '/' and self.cur_path[1] == '/':
                        self.cur_path = self.cur_path[1:]
                print(self.cur_dir)
                print(self.root_bin)
            
            elif command[0] == 'pwd':
                print(self.cur_path)
            
            elif command[0] == 'exit':
                print('bye,', self.cur_terminaluser.get_name())

            elif command[0] == 'cp':
                self.copy_command(command, self.cur_dir)
            
            elif command[0] == 'mv':
                self.move_command(command,self.cur_dir)

            elif command[0] == 'rm':
                self.remove_command(command,self.cur_dir)

            elif command[0] == 'rmdir':
                self.removeDir_command(command,self.cur_dir)

            elif command[0] == 'adduser':
                self.adduser_command(command,self.users, self.cur_terminaluser)
            
            elif command[0] == 'deluser':
                self.delususer_command(command,self.users,self.cur_terminaluser)

            elif command[0] == 'su':
                self.su_command(command,self.users,self.cur_terminaluser)


            else: print('Bad option')


    def mkdir_command(self,command,cur_dir):
        if len(command) == 1:
            print('mkdir: Invalid syntax')
        elif len(command) == 2: 
            result = self.analize_string(command[1])
            counter = 0
            #cur_dict = self.root
            aux = cur_dir
            for i in range(len(result)):
                keys = list(aux.keys())
                keys = [str(x) for x in keys]
                object_keys = list(aux.keys())

                if result[i] in keys:
                    indice = keys.index(result[i])
                    if object_keys[indice].get_type() == 'd':
                        aux = aux[object_keys[indice]]
                    else:
                        print('mkdir: Ancestor directory does not exist')
                        break
                    counter += 1
                elif result[i] not in keys and i == len(result)-1:
                    self.folder = Folder(result[i])
                    aux[self.folder] = {}
                else:
                    print('mkdir: Ancestor directory does not exist')
                    break
            if counter == len(result):
                    print('mkdir:file exists')
        elif len(command) == 3:
            if command[1] == '-p':
                result = self.analize_string(command[2])
                aux = cur_dir
                if isinstance(result,list):
                    aux = cur_dir
                    print(aux)
                    keys = list(aux.keys())
                    keys = [str(x) for x in keys]
                    object_keys = list(aux.keys()) 
                    for i in range(len(result)):
                        #print(keys)
                        if result[i] in keys:
                            indice = keys.index(result[i])
                            if object_keys[indice].get_type() == 'd':
                                aux = aux[object_keys[indice]]
                            else:
                                self.folder = Folder(result[i])
                                aux[self.folder] = {}
                                aux = aux[self.folder]
                        else:
                            self.folder = Folder(result[i])
                            aux[self.folder] = {}
                            aux = aux[self.folder]
                            #print(aux)
                    #print(self.root)
            else:
                print('mkdir: Invalid syntax')

    def touch_command(self,command,cur_dir):
        if len(command) == 1:
            print('touch: Invalid Syntax')
        elif len(command) == 2:
            result = self.analize_string(command[1])
            aux = cur_dir
            counter = 0
            for i in range(len(result)):
                keys = list(aux.keys())
                keys = [str(x) for x in keys]
                object_keys = list(aux.keys()) 
                if result[i] in keys:
                    indice = keys.index(result[i])
                    if object_keys[indice].get_type() == 'd':
                        aux = aux[object_keys[indice]]
                        counter += 1
                    else:
                        pass
                else:
                    self.file = File(result[i])
                    aux[self.file] = None

    def cd_command(self, command, cur_dir, cur_path):
        if len(command) == 1:
            self.cur_path = '//'
            self.cur_dir = self.root
        elif len(command) == 2:
            result = self.analize_string(command[1])
            if result[0] == '':
                del result[0]
            dir_inicial = cur_dir
            path_inicial = cur_path
            for i in range(len(result)):
                print(result[i])
                a = self.cd_enter_out(result[i],self.cur_dir,self.cur_path)
                if a == 1 :
                    print('cd: No such file or directory')
                    self.cur_dir = dir_inicial
                    self.cur_path = path_inicial
                    break
                elif a == 2:
                    print('cd: Destination is a file')
                    self.cur_dir = dir_inicial
                    self.cur_path = path_inicial
                    break
            print(self.cur_path)

    def cd_enter_out(self,result,cur_dir, cur_path):
        keys = list(cur_dir.keys())
        keys = [str(x) for x in keys]
        object_keys = list(cur_dir.keys()) 
        if result in keys:
            indice = keys.index(result)
            if object_keys[indice].get_type() == 'd':
                cur_dir = cur_dir[object_keys[indice]]
                cur_path = cur_path +  '/' + result 
                self.cur_dir = cur_dir
                self.cur_path = cur_path
            else:
                flag = 2
                return flag
            print('current path')
            print(cur_path)
        elif result == '..':
            slashes = [pos for pos,char in enumerate(cur_path) if char == '/']
            if len(slashes) == 1:
                cur_path = '//'
            else:
                #Imprime el path hasta antes de la ultima slash
                cur_path = cur_path[:max(slashes)]
            self.cur_path = cur_path
            print('Current path ..')
            print(cur_path)
            
            if cur_path == '/':
                aux = self.root_bin
                result = ['/']
                print('Regresamos al origen tenemos que entrar')
                print(result)
            else:
                aux = self.root
                print('esto tiene aux osea igual a root')
                print(aux)
                result = self.analize_string(self.cur_path)
                print(result)
                result = result[2:]
                print(result)
            if isinstance(result,list):
                for i in range(len(result)):
                    keys = list(aux.keys())
                    keys = [str(x) for x in keys]
                    object_keys = list(aux.keys()) 
                    if result[i] in keys:
                        indice = keys.index(result[i])
                        aux = aux[object_keys[indice]]
                        self.cur_dir = aux
                        print('Current dictionay')
                        print(self.cur_dir)
        elif result == '.' :
            pass        
        else:
            flag = 1
            return flag



    def copy_command(self, command, cur_dir):

        self.objeto = 0
        self.destino = 0
        self.name = ''
        
        if len(command) < 3:
            print('cp: incorrect syntax')

        #Analize path 1 path y termina con file
        aux1 = cur_dir
        print('esto tiene aux1')
        print(aux1)
        result = self.analize_string(command[1])
        a = self.determinant_source(result,aux1)
        print('esto tiene el source')
        print(a)
        print(self.objeto)

        if a == 1:
            #Encontramos el archivo
            result2 = self.analize_string(command[2])
            b = self.determinant_dest(result2,aux1)
            print('Esto tiene el destino')
            print(b)
            print(self.destino)
            if b == 1 :
                pass
            elif b == 2:
                print('entre aqui a cambiar el objeto')
                # Crear un nuevo objeto
                self.copy_file = Folder(self.name)
                self.copy_file.type_file = self.objeto.get_type()
                self.copy_file.read_ow = self.objeto.get_row()
                self.copy_file.write_ow = self.objeto.get_wow()
                self.copy_file.execute_ow = self.objeto.get_xow()

                self.copy_file.read_ot = self.objeto.get_rot()
                self.copy_file.write_ot = self.objeto.get_wot()
                self.copy_file.execute_ot = self.objeto.get_xot()
                print(self.objeto.get_type())
                self.destino[self.copy_file] = None
                print(self.destino)


    def determinant_source(self, result, aux1):
        for i in range(len(result)):
            keys = list(aux1.keys())
            keys = [str(x) for x in keys]
            object_keys = list(aux1.keys()) 
            
            print(object_keys)
            print('Result actual', result[i])
            if result[i] in keys:
                indice = keys.index(result[i])
                print('entre aqui')
                if i == len(result) - 1:
                    print('Y luego aqui')
                    if object_keys[indice].get_type() == 'd':
                        print('cp: Source is a directory')
                        break
                    else:
                        print('cp: File exists')
                        flag = 1
                        self.objeto = object_keys[indice]
                        return flag
                else:
                    print('LLegue al else')
                    aux1 = aux1[object_keys[indice]]
                    print('eL NUEVO diccionario es')
                    print(aux1)  
                    print('sus llaves son')
                    print(aux1.keys())  
            else:
                #En algun punto la ruta no existio
                print('cp: No such file')

    def determinant_dest(self, result, aux1):
        print('Llegue aqui')
        for i in range(len(result)):
            keys = list(aux1.keys())
            keys = [str(x) for x in keys]
            object_keys = list(aux1.keys()) 
            
            print(object_keys)
            print('Result actual', result[i])
            if result[i] in keys:
                indice = keys.index(result[i])
                print('entre aqui')
                if i == len(result) - 1:
                    print('Y luego aqui')
                    if object_keys[indice].get_type() == 'd':
                        print('cp: Destination is a directory')
                    else:
                        print('cp: File exist')
                        flag = 1
                        return flag
                else:
                    print('LLegue al else')
                    aux1 = aux1[object_keys[indice]]
                    print('eL NUEVO diccionario es')
                    print(aux1)  
                    print('sus llaves son')
                    print(aux1.keys()) 
            elif result[i] not in keys and i == len(result)-1:
                print('No existe eso es bueno')
                flag = 2
                self.destino = aux1
                self.name = result[i]
                return flag
            else:
                print('cp: No such file')
                return
                #En algun punto la ruta no existio

    def move_command(self, command, cur_dir):
        self.objeto = 0
        self.destino = 0
        self.original_source = 0
        self.name = ''
        
        if len(command) < 3:
            print('cp: incorrect syntax')

        #Analize path 1 path y termina con file
        aux1 = cur_dir
        print('esto tiene aux1')
        print(aux1)
        result = self.analize_string(command[1])
        a = self.determinant_source_mv(result,aux1)
        print('esto tiene el source')
        print(a)
        print(self.objeto)

        if a == 1:
            #Encontramos el archivo
            result2 = self.analize_string(command[2])
            b = self.determinant_dest_mv(result2,aux1)
            print('Esto tiene el destino')
            print(b)
            print(self.destino)
            if b == 1 :
                pass
            elif b == 2:
                print('entre aqui a cambiar el objeto')
                # Crear un nuevo objeto
                self.move_file = File(self.name)
                self.move_file.type_file = self.objeto.get_type()
                self.move_file.read_ow = self.objeto.get_row()
                self.move_file.write_ow = self.objeto.get_wow()
                self.move_file.execute_ow = self.objeto.get_xow()

                self.move_file.read_ot = self.objeto.get_rot()
                self.move_file.write_ot = self.objeto.get_wot()
                self.move_file.execute_ot = self.objeto.get_xot()

                self.destino[self.move_file] = None
                print(self.destino)
            elif b == 3:
                print('entre a recrear el objeto')
                print(self.objeto.get_name())
                self.move_file = File(self.objeto.get_name())
                self.move_file.type_file = self.objeto.get_type()
                self.move_file.read_ow = self.objeto.get_row()
                self.move_file.write_ow = self.objeto.get_wow()
                self.move_file.execute_ow = self.objeto.get_xow()

                self.move_file.read_ot = self.objeto.get_rot()
                self.move_file.write_ot = self.objeto.get_wot()
                self.move_file.execute_ot = self.objeto.get_xot()
                print(self.original_source)
                self.original_source[self.move_file] = None
                print(self.destino)


    def determinant_source_mv(self, result, aux1):
        print('Llegue aqui')
        for i in range(len(result)):
            keys = list(aux1.keys())
            keys = [str(x) for x in keys]
            object_keys = list(aux1.keys()) 
            
            print(object_keys)
            print('Result actual', result[i])
            if result[i] in keys:
                indice = keys.index(result[i])
                print('entre aqui')
                if i == len(result) - 1:
                    print('Y luego aqui')
                    if object_keys[indice].get_type() == 'd':
                        print('Source is a directory')
                    else:
                        print('Existe el file')
                        flag = 1
                        self.objeto = object_keys[indice]
                        print('Amooooos a borrarlo')
                        del aux1[object_keys[indice]]
                        self.original_source = aux1
                        print(aux1)
                        return flag
                else:
                    print('LLegue al else')
                    aux1 = aux1[object_keys[indice]]
                    print('eL NUEVO diccionario es')
                    print(aux1)  
                    print('sus llaves son')
                    print(aux1.keys())  
            else:
                #En algun punto la ruta no existio
                print('cp: No such file')


    def determinant_dest_mv(self, result, aux1):
        for i in range(len(result)):
            keys = list(aux1.keys())
            keys = [str(x) for x in keys]
            object_keys = list(aux1.keys()) 
            
            print(object_keys)
            print('Result actual', result[i])
            if result[i] in keys:
                indice = keys.index(result[i])
                print('entre aqui')
                if i == len(result) - 1:
                    print('Y luego aqui')
                    if object_keys[indice].get_type() == 'd':
                        print('Destination is a directory')
                    else:
                        print('cp: File exist')
                        flag = 1
                        return flag
                else:
                    print('LLegue al else')
                    aux1 = aux1[object_keys[indice]]
                    print('eL NUEVO diccionario es')
                    print(aux1)  
                    print('sus llaves son')
                    print(aux1.keys()) 
            elif result[i] not in keys and i == len(result)-1:
                print('No existe eso es bueno')
                flag = 2
                self.destino = aux1
                self.name = result[i]
                return flag
            else:
                print('En la ruta fallo')
                flag = 3
                return flag
                #En algun punto la ruta no existio


    def remove_command(self, command, cur_dir):
        if len(command) == 1:
            print('rm: Invalid Syntax')
        elif len(command) == 2:
            print('Entre al caso')
            result = self.analize_string(command[1])
            aux = cur_dir
            counter = 0
            for i in range(len(result)):
                print('entre aqui')
                keys = list(aux.keys())
                keys = [str(x) for x in keys]
                object_keys = list(aux.keys()) 
                if result[i] in keys:
                    print('entre al if')
                    indice = keys.index(result[i])
                    if i == len(result) - 1:
                        print('Y luego aqui')
                        if object_keys[indice].get_type() == 'd':
                            print('rm: Is is a directory')
                        else:
                            print('Existe el file')
                            print('Amooooos a borrarlo')
                            del aux[object_keys[indice]]
                            print(aux)
                    else:
                        print('LLegue al else')
                        aux = aux[object_keys[indice]]
                        print('eL NUEVO diccionario es')
                        print(aux)  
                        print('sus llaves son')
                        print(aux.keys())  
                else:
                    #En algun punto la ruta no existio
                    print('cp: No such file')    
                    break                
            print(cur_dir)

    def removeDir_command(self, command, cur_dir):
        if len(command) == 1:
            print('rmdir: Invalid Syntax')
        elif len(command) == 2:
            print('Entre al caso')
            result = self.analize_string(command[1])
            aux = cur_dir
            counter = 0
            for i in range(len(result)):
                print('entre aqui')
                keys = list(aux.keys())
                keys = [str(x) for x in keys]
                object_keys = list(aux.keys()) 
                if result[i] in keys:
                    print('entre al if')
                    indice = keys.index(result[i])
                    if i == len(result) - 1:
                        print('Y luego aqui')
                        if object_keys[indice].get_type() == 'd':
                            print('rm: Is is a directory')
                            print('Amooooos a borrarlo')
                            print (aux[object_keys[indice]])
                            if aux[object_keys[indice]]:
                                print('Hay algo ahi cabron namames')
                                break
                            else:
                                del aux[object_keys[indice]]
                            print(aux)
                        else:
                            print('rmdir: Not a directory')
                    else:
                        #Avanzamos
                        print('LLegue al else')
                        aux = aux[object_keys[indice]]
                        print('eL NUEVO diccionario es')
                        print(aux)  
                        print('sus llaves son')
                        print(aux.keys())  
                else:
                    #En algun punto la ruta no existio
                    print('rmdir: No such file or directory')    
                    break                
            print(cur_dir)
            

    def adduser_command(self, command ,user_list, current_user ):
        if current_user.get_name() != 'root':
            print("adduser: Operation not permitted") 
            return

        if len(command) == 1:
            print("adduser: Incorrect syntax")
        elif len(command) == 2:
            names = []
            #Comprobar si el usuario existe
            for i in range(len(user_list)):
                names.append(user_list[i].get_name())
            if command[1] in names:
                print('The user already exist')
            else:
                new_user = User(command[1])
                user_list.append(new_user)


    def delususer_command(self, command,user_list,current_user):
        if current_user.get_name() != 'root':
            print("deluser: Operation not permitted") 
            return

        if len(command) == 1:
            print("adduser: Incorrect syntax")
        elif len(command) == 2:
            names = []
            if command[1] == 'root':
                print('WARNING: You are just about to delete the root account Usually this is never required as it may render the whole system unusable If you really want this, call deluser with parameter --force (but this `deluser` does not allow `--force`, haha) Stopping now without having performed any action')
                return
            #Comprobar si el usuario existe
            for i in range(len(user_list)):
                names.append(user_list[i].get_name())
            if command[1] in names:
                indice = names.index(command[1])
                del user_list[indice]
            else:
                print('deluser: The user does not exist')
            print(user_list)

    def su_command(self,command,user_list,current_user):
        if len(command) == 1:
            self.cur_terminaluser = self.root_user
        elif len(command) == 2:
            names = []
            #Comprobar si el usuario existe
            for i in range(len(user_list)):
                names.append(user_list[i].get_name())
            if command[1] in names:
                indice = names.index(command[1])
                current_user  = user_list[indice]
                self.cur_terminaluser = current_user
            else:
                print('su: Invalid user')

    def ls_command(self,command):
        if len(command) == 1:
            print(len(command))

    def analize_string(self, string):
        if '/' in string:
            string = string.split('/')
            #Array of words that define path
            return string
        else:
            #Name of file to be created
            string = string.split()
            return string

    def print_dic(self):
        for key, obj in self.root.items():
            print(key, '-->', obj)


if __name__ == "__main__": 
    try:
        Terminal()
    except:
        pass