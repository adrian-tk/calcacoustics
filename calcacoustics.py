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
from kivy.uix.button import Button

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
        self.speaker_qts["EBP"]["value"].text=str(ans["value"])

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

    def open_description(self, event):
        #TODO
        for key, val in self.speaker_qts.items():
            if val == event:
                #print(self.speaker_desclab[key])
                #self.speaker_desclab[key].size_hint=(None, 0.5)
                self.speaker_qts[key]['desc_label'].size=(0, 0)

    def build(self):
        """ buld views of GUI
        accrodion type
        """
        root=Accordion()
        self.inf=interface.Interface()
        # Speaker part
        # speaker data, mostly from poducer
        # some calculation of ESP etc.
        # values from object setting in a loop
        # changeable object for values holded in dictionary
        speaker_item=AccordionItem(title="Speaker")
        speaker_layout=BoxLayout(orientation="vertical")
        # Ask iterface about list of parameters
        # return a dictionary of dictionaries
        ans=self.inf.send({
            "section": "speaker",
            "item": "list_quantities",
            "action": "get",
            "value": None,
            })
        # a lot of info below
        #logging.debug(f"answer from calc: {ans}")

        # dictionary of dictionaries to hold
        # data from widget created in loop
        # ie: {Qts: {unit: <some object>}}
        self.speaker_qts={}
        # outside loop for get quantity
        for key, val in ans.items():
            # dict for widgets in quantity
            qty_widgets={}
            # BoxLayout for quantity
            # top: name, short name, value, unit etc.
            # bottom to hide with help, and block
            all_layout = BoxLayout(
                    orientation='vertical',
                    size=(500, 30),
                    size_hint = (1, None )
                    )
            top_layout = BoxLayout(
                    orientation="horizontal",
                    )
            bottom_layout = BoxLayout(
                    orientation="horizontal",
                    )
            qty_widgets.update({
                    'all_layout': all_layout,
                    'top_layout': top_layout,
                    'bottom_layout': bottom_layout
                    })
            # internal loop for populate each quantity
            for ikey, ival in ans[key].items():
                match ikey:
                    case "desc":
                        desc_btn=Button(
                             text='V',
                             size=(
                                all_layout.height,
                                all_layout.height,
                                ),
                             size_hint=(None, None),
                             )
                        desc_btn.bind(on_press=self.open_description)
                        top_layout.add_widget(desc_btn)
                        desc_label = Label(text=str(ival))
                        bottom_layout.add_widget(desc_label)

                        qty_widgets.update({
                            'desc_btn': desc_btn,
                            'desc_label': desc_label
                            })

                    case "value":
                        qty_val = FloatInput(
                            multiline=False,
                            text=str(ival),
                            )
                        qty_val.kname = key
                        qty_val.bind(text=self.num_val_update)
                        top_layout.add_widget(qty_val)

                        qty_widgets.update({
                            'value': qty_val,
                            })
                                
                    case default:
                        tmp_q = Label(text=str(ival))
                        top_layout.add_widget(tmp_q)

                        qty_widgets.update({
                            ikey: tmp_q,
                            })


            self.speaker_qts.update({key: qty_widgets})
            # iterate for one quantity do show all widget
            all_layout.add_widget(top_layout)
            #big_quant_layout.add_widget(bottom_quant_layout)
            speaker_layout.add_widget(all_layout)
        self.tmpans = Label(text="END")
        speaker_layout.add_widget(self.tmpans)
        speaker_item.add_widget(speaker_layout)
        root.add_widget(speaker_item)
        #Enclosure
        enclosure_item=AccordionItem(title="Enclosure")
        enclosure_item.add_widget(Label(text="Enclosure data and calculation"))
        root.add_widget(enclosure_item)
        # open speaker item as default when running program
        speaker_item.collapse=False
        return root

if __name__=="__main__":
    CalcAcousticsApp().run()
