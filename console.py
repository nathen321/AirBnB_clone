#!/usr/bin/python3
"..."
import re
from shlex import split
import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """..."""

    prompt = '(hbnb) '
    classes = {
            "BaseModel", "User", "State", "City", "Place", "Amenity", "Review"
            }

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def do_create(self, arg):
        """..."""
        arge = parse(arg)
        if len(arge) == 0:
            print("** class name missing **")
        elif arge[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            print(eval(arge[0])().id)
            storage.save()

    def do_destroy(self, arg):
        """..."""
        arge = parse(arg)
        objdict = storage.all()
        if len(arge) == 0:
            print("** class name missing **")
        elif arge[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(arge) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arge[0], arge[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(arge[0], arge[1])]
            storage.save()

    def do_all(self, arg):
        """..."""
        to_print = []
        if not arg:
            for obj in storage.all().values():
                to_print.append(obj.__str__())
        else:
            if arg not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return False
            else:
                for obj in storage.all().values():
                    if arg == obj.__class__.__name__:
                        to_print.append(obj.__str__())
        print(to_print)

    def do_update(self, arg):
        """..."""
        arge = parse(arg)
        dicte = storage.all()
        if len(arge) == 0:
            print("** class name missing **")
            return False
        if arge[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return False
        if len(arge) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arge[0], arge[1]) not in dicte.keys():
            print("** no instance found **")
            return False
        if len(arge) == 2:
            print("** attribute name missing **")
            return False
        if len(arge) == 3:
            print("** value missing **")
            return False

        if len(arge) == 4:
            obj = dicte["{}.{}".format(arge[0], arge[1])]
            if arge[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[arge[2]])
                obj.__dict__[arge[2]] = valtype(arge[3])
            else:
                obj.__dict__[arge[2]] = arge[3]

    def do_show(self, arg):
        """..."""
        arge = parse(arg)
        dicte = storage.all()
        if len(arge) == 0:
            print("** class name missing **")
        elif arge[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(arge) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arge[0], arge[1]) not in dicte:
            print("** no instance found **")
        else:
            print(dicte["{}.{}".format(arge[0], arge[1])])


if __name__ == '__main__':
    HBNBCommand().cmdloop()
