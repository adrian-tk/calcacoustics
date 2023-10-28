#! env/bin/python

# import logging stuff at first
try:
    from logger import logging
    from logger import logger
    from logger import logcom
    logger.debug("imported loggers")
except Exception as err:
    print("Can't import loggers")
    print(err)
    print("maybe You shold be in env?")

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import interface
from kivy_common import FloatInput

# print available loggers
loggers = [logging.getLogger(name) for name in \
        logging.root.manager.loggerDict]
for logg in loggers:
    logger.debug(logg)

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
        logger.debug(f"value: {value}, key: {instance.kname} updated in GUI")
        ans=self.inf.send({
            "section": "speaker",
            "item": instance.kname,
            "action": "set",
            "value": value,
            })
        self.tmpans.text=value
        self.calc_update()

    def open_description(self, event):
        for key, val in self.speaker_qts.items():
            if val['desc_btn'] == event:
                #print (self.speaker_qts[key])
                logger.debug(f"key: {key} pressed")
                a=self.speaker_qts[key]
                if a['desc_label'].disabled:
                    a['bottom_layout'].size[1] = 70
                    a['all_layout'].size[1] = 100
                    a['desc_label'].opacity=1
                    a['desc_label'].disabled=False
                    a['desc_label'].size = a['bottom_layout'].size
                    a['desc_label'].text_size = a['desc_label'].size
                    #print(a['desc_label'].text_size)
                else:
                    a['bottom_layout'].size=(500,0 )
                    a['all_layout'].size=(500, 30)
                    a['desc_label'].opacity=0
                    a['desc_label'].disabled=True

    def build(self):
        """ buld views of GUI
        accrodion type
        """
        HEIGHT=30
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
        #logger.debug(f"answer from calc: {ans}")

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
                    size=(500, HEIGHT),
                    size_hint = (1, None )
                    )
            top_layout = BoxLayout(
                    orientation="horizontal",
                    size=(500, all_layout.height),
                    size_hint = (1, None )
                    )
            bottom_layout = BoxLayout(
                    orientation="horizontal",
                    size=(500, 0),
                    size_hint = (1, None )
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
                        desc_label = Label(
                                text=str(ival),
                                valign = 'top',
                                padding = [5, 5, 5, 5]
                                )
                        bottom_layout.add_widget(desc_label)
                        desc_label.disabled=True
                        desc_label.opacity=0

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
            all_layout.add_widget(top_layout)
            all_layout.add_widget(bottom_layout)
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
