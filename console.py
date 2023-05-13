#!/usr/bin/python3
"""
This module defines a command interpreter class to manage the Airbnb project.
"""

import cmd
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import models
import re


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter class to manage the Airbnb project.
    """
    prompt = '(hbnb) '

    def do_quit(self, arg):
        """
        Quit command to exit the program.
        """
        return True

    def do_EOF(self, arg):
        """
        Exit the program at end of file.
        """
        return True

    def emptyline(self):
        """
        Do nothing when empty line is entered.
        """
        pass

    def do_create(self, arg):
        """
        Create a new instance of BaseModel, save it to the JSON file and print
        its id.
        """
        if not arg:
            print("** class name missing **")
        elif arg not in models.class_dict:
            print("** class doesn't exist **")
        else:
            obj = models.class_dict[arg]()
            obj.save()
            print(obj.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance based on the class name
        and id.
        """
        args = arg.split()
        if not arg:
            print("** class name missing **")
        elif args[0] not in models.class_dict:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            if key not in models.storage.all():
                print("** no instance found **")
            else:
                print(models.storage.all()[key])

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id, and save the changes
        into the JSON file.
        """
        args = arg.split()
        if not arg:
            print("** class name missing **")
        elif args[0] not in models.class_dict:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            if key not in models.storage.all():
                print("** no instance found **")
            else:
                models.storage.all().pop(key)
                models.storage.save()

    def do_all(self, arg):
        """
        Prints all string representations of all instances based or not on the
        class name.
        """
        if not arg:
            print([str(v) for v in models.storage.all().values()])
        elif arg not in models.class_dict:
            print("** class doesn't exist **")
        else:
            print([str(v) for v in models.storage.all()])

    def do_update(self, arg):
        """
    Updates an instance based on the class name and id by adding or
    updating attribute (save the change into the JSON file).
    Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
    # Use regular expressions to parse the command input
        match = re.match(r'^update (\w+) (\w+) (\w+) (.+)$', arg)
        if match:
            class_name = match.group(1)
            instance_id = match.group(2)
            attribute_name = match.group(3)
            attribute_value = match.group(4).strip('"')

        # Get the instance from the data store
        instance = self.storage.get(class_name, instance_id)

        if instance is None:
            print("** no instance found **")
            return

        # Update the attribute value
        setattr(instance, attribute_name, attribute_value)

        # Save the changes to the data store
        self.storage.save()

        else:
        print("** invalid update syntax **")

    def do_count(self, arg):
        """
        Retrieve the number of instances of a class.
        """
        if not arg:
            print("** class name missing **")
        elif arg not in models.class_dict:
            print("** class doesn't exist **")
        else:
            print(len(models.class_dict[arg].all()))

    def do_show(self, arg):
        """
        Retrieve an instance based on its ID.
        """
        args = arg.split()
        if not arg:
            print("** class name missing **")
        elif args[0] not in models.class_dict:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            if key not in models.storage.all():
                print("** no instance found **")
            else:
                print(models.storage.all()[key])

    def default(self, arg):
        """
        Default method called when the command entered is not recognized.
        """
        args = arg.split(".")
        if len(args) > 1:
            if args[1] == "all()":
                self.do_all(args[0])
            elif args[1] == "count()":
                self.do_count(args[0])
            elif args[1].startswith("show(") and args[1].endswith(")"):
                id = args[1][5:-1]
                self.do_show("{} {}".format(args[0], id))
            elif args[1].startswith("destroy(") and args[1].endswith(")"):
                id = args[1][8:-1]
                self.do_destroy("{} {}".format(args[0], id))
            elif args[1].startswith("update(") and args[1].endswith(")"):
                update_args = args[1][7:-1].split(", ")
                if len(update_args) < 2:
                    print("** dictionary missing **")
                else:
                    id = update_args[0][1:-1]
                    update_dict = update_args[1]
                    self.do_update("{} {} {}".format(args[0], id, update_dict))
            else:
                print("** invalid command **")
        else:
            print("** invalid command **")


if __name__ == '__main__':
    '''command loop'''
    HBNBCommand().cmdloop()
