#! env/bin/python

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.accordion import Accordion, AccordionItem

class CalcAcousticsApp(App):

    def build(self):
        root=Accordion()
        #Speaker
        speaker_item=AccordionItem(title="Speaker")
        speaker_item.add_widget(Label(text="Speaker data and calculation"))
        root.add_widget(speaker_item)
        #Enclosure
        enclosure_item=AccordionItem(title="Enclosure")
        enclosure_item.add_widget(Label(text="Enclosure data and calculation"))
        root.add_widget(enclosure_item)
        return root

if __name__=="__main__":
    CalcAcousticsApp().run()
