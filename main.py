import csv
import io
import os
import subprocess
import sys

import inquirer
from inquirer import errors


class Main:
    def __init__(self,file="./test.csv"):
        self.file = file
        self.checklist = []
        self.update()

    def validate(self, answers, current):
        # print(f"TESTING: {current}")
        if len(current) == 0:
            raise inquirer.errors.ValidationError(answers,reason="Length too small")
        else:
            return True
    def add(self):
        question =  [
            inquirer.Text(
                "Item",
                message="What do you wish to add to your checklist",validate=self.validate
            )
        ]
        result = inquirer.prompt(question)
        if result['Item'] is None:
            return
        self.checklist.append(
            [
                "", # ignore this
                result['Item'],
                "Not Done"
            ]
        )
        self.write()

    def read(self):
        with open(self.file, "r") as f:
            x = csv.reader(f)
            self.checklist = [] # reset checklist
            try:
                for row in x:
                    self.checklist.append(row)
            except io.UnsupportedOperation as e:
                print(f"Error, {e}")
                input()

    def write(self):
        with open(self.file, "w") as f:
            x = csv.writer(f)
            x.writerows(self.checklist)
        # print("Written successfully")

    def update(self):
        self.read()

    def complete_task(self):
        z = []
        for x in range(len(self.checklist)):
            z.append([str(x)+': '+self.checklist[x][1]+' Status: '+self.checklist[x][2]])
        questions = [inquirer.Checkbox('option',message="Item to toggle",choices=z)]
        answers = inquirer.prompt(questions)
        # print(answers)
        if len(answers['option']) == 0:
            return
        for item in answers['option'][0]:
            index = int(item.split(":")[0])
            x = self.checklist[index][2]
            # print(x)
            if x.lower() == "not done":
                self.checklist[index][2] = "Done"
            else:
                self.checklist[index][2] = "Not Done"


    def listing(self):
        for item in self.checklist:
            print("> " + item[1], "Status:" + " " + item[2],sep=", ")

    def remove(self): # remove an item from the checklist
        z = []
        for x in range(len(self.checklist)):
            z.append([str(x)+': '+self.checklist[x][1]])


        questions = [inquirer.List('option',message="Item to remove",choices=z)]
        answers = inquirer.prompt(questions)
        if answers is not None:
            # print(type(answers))
            # print(answers)
            self.checklist.pop(int(answers['option'][0].split(':')[0]))
            self.write()

    def clear_screen(self):
        subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)

    def main(self):
        while True:
            self.clear_screen()
            # inquirer get options menu
            questions = [
                inquirer.List(
                "menu", message="Choose an option", choices = ["Add item to checklist","Remove item from checklist", "List the checklist items","Complete a task!", "Quit"], carousel=True
                ),

            ]
            result = inquirer.prompt(questions)
            if result['menu'] is not None:
                choice = result['menu']
                if "Add" in choice:
                    self.add()
                elif "Remove" in choice:
                    self.remove()
                elif "List" in choice:
                    self.listing()
                elif "Complete" in choice:
                    self.complete_task()
                elif "Quit" in choice:
                    sys.exit()
                else:
                    self.listing()
                # check what to perform
                input("Press enter to continue")

Main().main()





