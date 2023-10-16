#! env/bin/python

LOGFORMAT="%(levelname)-8s[%(name)s]\
     [%(filename)s][%(funcName)s] %(message)s"
LOGFILEFORMAT="%(asctime)s - %(levelname)-8s\
         [%(name)s][%(filename)s:%(lineno)d]\
         [%(funcName)s] %(message)s"

import logging
logging.basicConfig(format=LOGFORMAT, level=logging.DEBUG)
import re

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

import interface

class FloatInput(TextInput):
    kname=""
    pat=re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat=self.pat
        if '.' in self.text:
            s = re.sub(pat, "", substring)
        else:
            s = '.'.join(
                    re.sub(pat, "", s)
                    for s in substring.split('.', 1)
                    )
        return super().insert_text(s, from_undo=from_undo)

class CalcAcousticsApp(App):

    def calc_update(self):
        ans=self.inf.send({
            "section": "speaker",
            "item": 'EBP',
            "action": "calculate",
            "value": "",
            })
        print((ans['value']))

    def num_val_update(self, instance, value):
        logging.debug(f"value: {value}, key: {instance.kname} updated in GUI")
        ans=self.inf.send({
            "section": "speaker",
            "item": instance.kname,
            "action": "set",
            "value": value,
            })
        self.tmpans.text=value
        self.calc_update()

    def build(self):
        root=Accordion()
        self.inf=interface.Interface()
        #Speaker
        QUANT_HEIGHT=10
        speaker_item=AccordionItem(title="Speaker")
        speaker_layout=BoxLayout(orientation="vertical")
        ans=self.inf.send({
            "section": "speaker",
            "item": "list_quantities",
            "action": "get",
            "value": None,
            })
        #logging.debug(f"answer from calc: {ans}")
        for key, val in ans.items():
            quantity_layout=BoxLayout(orientation="horizontal",
                                      size = (500, 30),
                                      size_hint = (1, None))
            for ikey, ival in ans[key].items():
                match ikey:
                    case "desc":
                        # don't show description
                        pass
                    case "value":
                        quant_val=FloatInput(
                                multiline=False,
                                size=(100,30),
                                size_hint=(None, None),
                                text=str(ival),
                                )
                        quant_val.kname = key
                        quant_val.bind(text=self.num_val_update)
                        quantity_layout.add_widget(quant_val)
                    case default:
                        quantity_layout.add_widget(Label(text=str(ival)))
            speaker_layout.add_widget(quantity_layout)
        self.tmpans = Label(text="END")
        speaker_layout.add_widget(self.tmpans)
        speaker_item.add_widget(speaker_layout)
        root.add_widget(speaker_item)
        #Enclosure
        enclosure_item=AccordionItem(title="Enclosure")
        enclosure_item.add_widget(Label(text="Enclosure data and calculation"))
        root.add_widget(enclosure_item)
        return root

if __name__=="__main__":
    CalcAcousticsApp().run()
