import os
import json
import io
import argparse


class FlashCard:
    my_dict = dict()
    log_errors = dict()

    def __init__(self):
        # создаем буфер для записи
        self.buffer = io.StringIO()

    def cards_add(self):
        term = self.check_term(input('The card:\n'), self.my_dict, self.buffer)
        self.add_buffer('The card:\n')
        definition = self.check_definition(input('The definition of the card:\n'), self.my_dict, self.buffer)
        self.add_buffer('The definition of the card:\n')
        self.my_dict[term] = definition
        self.log_errors[term] = 0
        print(f'The pair ("{term}":"{definition}") has been added.\n')
        self.add_buffer(f'The pair ("{term}":"{definition}") has been added.\n')

    def cards_remove(self):
        card = input('Which card?\n')
        self.add_buffer('Which card?\n')
        if card in self.my_dict:
            self.my_dict.pop(card)
            print('The card has been removed.\n')
            self.add_buffer('The card has been removed.\n')
        else:
            print(f'Can\'t remove "{card}": there is no such card.\n')
            self.add_buffer(f'Can\'t remove "{card}": there is no such card.\n')

    def cards_import(self):
        ans = input('File name:\n')
        self.add_buffer('File name:\n')
        if not os.path.isfile(ans):
            print("File not found.\n")
            self.add_buffer("File not found.\n")
        else:
            with open(ans, "r") as f:
                my_string = f.read()
                cards = json.loads(my_string.replace("'", "\""))
                for key, value in cards.items():
                    self.my_dict[key] = value
                print(f'{len(cards)} cards have been loaded.\n')
                self.add_buffer(f'{len(cards)} cards have been loaded.\n')

    def cards_args_import(self, args):
        if not os.path.isfile(args):
            pass
        else:
            with open(args, "r") as f:
                my_string = f.read()
                cards = json.loads(my_string.replace("'", "\""))
                for key, value in cards.items():
                    self.my_dict[key] = value
                    self.log_errors[key] = 0
                print(f'{len(cards)} cards have been loaded.\n')

    def cards_export(self):
        ans = input('File name:\n')
        self.add_buffer('File name:\n')
        with open(ans, 'w') as file:
            file.write(str(self.my_dict))
        print(f'{len(self.my_dict)} cards have been saved.\n')
        self.add_buffer(f'{len(self.my_dict)} cards have been saved.\n')

    def cards_args_export(self, args):
        with open(args, 'w') as file:
            file.write(str(self.my_dict))
        print(f'{len(self.my_dict)} cards have been saved.\n')

    def cards_log(self):
        ans = input('File name:')
        self.add_buffer('File name:\n')
        res = self.buffer.getvalue()
        with open(ans, 'w') as file:
            file.write(res)
        print('The log has been saved.\n')
        self.add_buffer('The log has been saved.\n')

    def hardest_card(self):
        try:
            max_value = max(self.log_errors.values())
            max_keys = [k for k, v in self.log_errors.items() if v == max_value]
            if len(max_keys) == 0 or max_value == 0:
                print('There are no cards with errors.\n')
                self.add_buffer('There are no cards with errors.\n')
            elif len(max_keys) == 1 and max_value > 0:
                print(f'The hardest card is "{max_keys[0]}". You have {max_value} errors answering it.\n')
                self.add_buffer(f'The hardest card is "{max_keys[0]}". You have {max_value} errors answering it.\n')
            elif len(max_keys) > 1 and max_value > 0:
                print(f'The hardest card is "{max_keys}". You have {max_value} errors answering it.\n')
                self.add_buffer(f'The hardest card is "{max_keys}". You have {max_value} errors answering it.\n')
        except ValueError:
            print('There are no cards with errors.\n')
            self.add_buffer('There are no cards with errors.\n')

    def cards_reset_stats(self):
        self.log_errors = dict.fromkeys(self.log_errors, 0)
        print('Card statistics have been reset.\n')
        self.add_buffer('Card statistics have been reset.\n')

    def cards_ask(self):
        count = int(input('How many times to ask?\n'))
        self.add_buffer('How many times to ask?\n')
        while count != 0:
            for key in self.my_dict:
                answer = input(f'Print the definition of "{key}":\n')
                if self.my_dict[key] == answer:
                    print('Correct!\n')
                    self.add_buffer('Correct!\n')
                else:
                    self.log_errors[key] += 1
                    definition = self.my_dict[key]
                    if answer in self.my_dict.values():
                        for key_, value in self.my_dict.items():
                            if value == answer:
                                print(
                                    f'Wrong. The right answer is "{definition}", '
                                    f'but your definition is correct for "{key_}".\n')
                                self.add_buffer(f'Wrong. The right answer is "{definition}", '
                                                f'but your definition is correct for "{key_}".\n')
                    else:
                        print(f'Wrong. The right answer is "{definition}".\n')
                        self.add_buffer(f'Wrong. The right answer is "{definition}".\n')
                count -= 1
                if count == 0:
                    break

    def add_buffer(self, string):
        self.buffer.write(string)

    @staticmethod
    def check_term(_term, my_dict, buffer) -> str:
        if _term not in my_dict:
            return _term
        else:
            while _term in my_dict:
                print(f'The term "{_term}" already exists. Try again:')
                buffer.write(f'The term "{_term}" already exists. Try again:')
                _term = input()
            return _term

    @staticmethod
    def check_definition(_definition, my_dict, buffer) -> str:
        if _definition not in my_dict.values():
            return _definition
        else:
            while _definition in my_dict.values():
                print(f'The definition "{_definition}" already exists. Try again:')
                buffer.write(f'The definition "{_definition}" already exists. Try again:')
                _definition = input()
            return _definition

    @classmethod
    def check_my_dict(cls):
        for key in cls.my_dict:
            answer = input(f'Print the definition of "{key}":\n')
            if cls.my_dict[key] == answer:
                print('Correct!')
            else:
                definition = cls.my_dict[key]
                if answer in cls.my_dict.values():
                    for key_, value in cls.my_dict.items():
                        if value == answer:
                            print(
                                f'Wrong. The right answer is "{definition}", '
                                f'but your definition is correct for "{key_}".')
                else:
                    print(f'Wrong. The right answer is "{definition}".')


def running_methods(answer, card):
    ans_dict = {'add': card.cards_add,
                'remove':  card.cards_remove,
                'import': card.cards_import,
                'export': card.cards_export,
                'ask': card.cards_ask,
                'log': card.cards_log,
                'hardest card': card.hardest_card,
                'reset stats': card.cards_reset_stats}
    ans_dict[answer]()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--export_to")
    parser.add_argument("--import_from")

    args = parser.parse_args()

    card = FlashCard()

    if args.import_from is not None:
        card.cards_args_import(args.import_from)

    while True:
        answer = input('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n')
        card.add_buffer('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n')
        if answer == 'exit':
            print('Bye bye!')
            break
        running_methods(answer, card)

    if args.export_to is not None:
        card.cards_args_export(args.export_to)


if __name__ == "__main__":
    main()
