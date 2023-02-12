#!/usr/bin/python3
"""
This module contains the program for the entry point of the command interpreter
"""


import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):

    """
    This is the class that the command interpreter program
    operates on.
    """

    prompt = '(hbnb) '
    class_present = ['BaseModel', 'User', 'State', 'City',
                     'Amenity', 'Place', 'Review']

    def do_quit(self, arg):
        """
        Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """
        Quit command to exit the program
        """
        print("")
        return True

    def emptyline(self):
        """
        Prevents the previous command from being executed when
        and empty libe is passed
        """
        pass

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id.
        Ex: $ create BaseModel
        """
        args = list(arg.split())
        if len(args) == 0:
            print("** class name missing **")
            return
        elif args[0] not in HBNBCommand.class_present:
            print("** class doesn't exist **")
            return
        inst = eval(args[0])()
        inst.save()
        print(inst.id)

    def check_not_id(id):
        current_inst = storage.all()
        for keys, values in current_inst.items():
            if values['id'] == id:
                return False
        return True

    def do_show(self, arg):
        """
         Prints the string representation
         of an instance based on the class name and id.
         Ex: $ show BaseModel 1234-1234-1234.
        """
        args = list(arg.split())
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.class_present:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
            return
        key = args[0] + '.' + args[1]
        if key not in storage.all():
            print("** no instance found **")
        elif HBNBCommand.check_not_id(args[1]):
            print("** no instance found **")
        else:
            key = args[0] + '.' + args[1]
            instances = storage.all().copy()
            inst = eval(args[0])(**instances[key])
            print(inst)

    def do_destroy(self, arg):
        """
         Deletes an instance based on the class name and id
         (save the change into the JSON file).
         Ex: $ destroy BaseModel 1234-1234-1234.
        """
        args = list(arg.split())
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.class_present:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif HBNBCommand.check_not_id(args[1]):
            print("** no instance found **")
        else:
            key = args[0] + '.' + args[1]
            del storage.all()[key]
            storage.save()

    def do_all(self, arg):
        """
         Prints all string representation of all
         instances based or not on the class name.
         Ex: $ all BaseModel or $ all.
        """
        instances = storage.all().copy()
        str_all = []
        args = list(arg.split())
        if len(args) == 0:
            for a_class, info in instances.items():
                inst = eval(info['__class__'])(**info)
                str_all.append(inst.__str__())
        else:
            if args[0] not in HBNBCommand.class_present:
                print("** class doesn't exist **")
                return
            else:
                for a_class, info in instances.items():
                    if info['__class__'] == args[0]:
                        inst = eval(args[0])(**info)
                        str_all.append(inst.__str__())
        print(str_all)

    def do_update(self, arg):
        """
         Updates an instance based on the class name
         and id by adding or updating attribute
         (save the change into the JSON file).
         Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com".
        """
        args = list(arg.split())
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.class_present:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif HBNBCommand.check_not_id(args[1]):
            print("** no instance found **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        else:
            key = args[0] + '.' + args[1]
            value = args[3]
            if value[0] == '"' and value[-1] == '"':
                value = value[1:-1]
            if value.isdigit():
                value = int(value)
                # elif value.isfloat():
                #    value = float(value)
            storage.all()[key][args[2]] = value
            instance = storage.all()[key]
            inst = eval(args[0])(**instance)
            inst.save()
            storage.all()[key]['updated_at'] = inst.updated_at.isoformat()
            storage.save()

    def count(self, arg):
        """
         counts and the number of instances
         of a class.
        """
        instances = storage.all().copy()
        num_inst = 0
        args = list(arg.split())
        if len(args) == 0:
            print("** class name missing **")
        else:
            if args[0] not in HBNBCommand.class_present:
                print("** class doesn't exist **")
                return
            else:
                for a_class, info in instances.items():
                    if info['__class__'] == args[0]:
                        num_inst += 1
        print(num_inst)

    def default(self, arg):
        """
        This method deals with the following commands
        <class name>.all(),
        <class name>.count(),
        <class name>.show(<id>),
        <class name>.destroy(<id>),
        <class name>.update(<id>, <attribute name>, <attribute value>),
        <class name>.update(<id>, <dictionary representation>).
        """
        if "." not in arg or "(" not in arg or len(arg) < 10:
            print("** command not found **" )
            return

        args = arg.split(".")
        brace_idx = args[1].index('(')
        cmds = args[1][:brace_idx]
        arg = args[1].split("(")
        arg = arg[1][:-1]
        arg_line = arg.split(", ")
        argv = ""
        if len(arg_line) != 0:
            for a in arg_line:
                if not a.isdigit():
                    a = a[1:-1]
                argv += a + " "
        if cmds == "count":
            self.count(args[0] + " " + argv)
            return

        eval("self.do_" + cmds)(args[0] + " " + argv)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
