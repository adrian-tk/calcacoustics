#! env/bin/python

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.accordion import Accordion, AccordionItem
import json
import interface

class CalcAcousticsApp(App):

    def build(self):
        root=Accordion()
        inf=interface.Interface()
        #Speaker
        speaker_item=AccordionItem(title="Speaker")
        ans=inf.send(json.dumps({"speaker": "list_quantities"}))
        print (ans)
        dec=json.loads(ans)
        print(dec)
        for x in dec:
            speaker_item.add_widget(Label(text=x))
        #speaker_item.add_widget(Label(text="Speaker data and calculation"))
        root.add_widget(speaker_item)
        #Enclosure
        enclosure_item=AccordionItem(title="Enclosure")
        enclosure_item.add_widget(Label(text="Enclosure data and calculation"))
        root.add_widget(enclosure_item)
        return root

if __name__=="__main__":
    CalcAcousticsApp().run()
