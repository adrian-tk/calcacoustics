#! env/bin/python

LOGFORMAT="%(levelname)-8s[%(name)s]\
     [%(filename)s][%(funcName)s] %(message)s"
LOGFILEFORMAT="%(asctime)s - %(levelname)-8s\
         [%(name)s][%(filename)s:%(lineno)d]\
         [%(funcName)s] %(message)s"

import logging
logging.basicConfig(format=LOGFORMAT, level=logging.DEBUG)
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
import interface


class CalcAcousticsApp(App):

    def build(self):
        root=Accordion()
        inf=interface.Interface()
        #Speaker
        speaker_item=AccordionItem(title="Speaker")
        speaker_layout=BoxLayout(orientation="vertical")
        ans=inf.send({"speaker": "list_quantities"})
        logging.debug(f"answer from calc: {ans}")
        for key, val in ans.items():
            quantity_layout=BoxLayout(orientation="horizontal")
            for ikey, ival in ans[key].items():
                match ikey:
                    case "desc":
                        # don't show description
                        pass
                    case "value":
                        # don't show description
                        quantity_layout.add_widget(TextInput(multiline=False))
                        pass
                    case default:
                        quantity_layout.add_widget(Label(text=str(ival)))
            #speaker_layout.add_widget(Label(text=key))
            speaker_layout.add_widget(quantity_layout)
        #speaker_item.add_widget(Label(text="Speaker data and calculation"))
        speaker_item.add_widget(speaker_layout)
        root.add_widget(speaker_item)
        #Enclosure
        enclosure_item=AccordionItem(title="Enclosure")
        enclosure_item.add_widget(Label(text="Enclosure data and calculation"))
        root.add_widget(enclosure_item)
        return root

if __name__=="__main__":
    CalcAcousticsApp().run()
