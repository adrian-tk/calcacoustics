#! env/bin/python

# import logging stuff at first
try:
    from logger import logging
    from logger import logger
    from logger import logcom
    logger.debug("imported loggers")
    from logger import setlog
    setlog('debug')
    #setlog('all')
except Exception as err:
    print("Can't import loggers")
    print(err)
    print("maybe You shold be in env?")

import os

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView


import interface
from kivy_common import FloatInput
from kivy_common import DescButton

# print available loggers
loggers = [logging.getLogger(name) for name in \
        logging.root.manager.loggerDict]
for logg in loggers:
    logger.debug(logg)

class CalcAcousticsApp(App):

    def val_get(self, item):
        ans=self.inf.send({
            "section": "speaker",
            "item": item,
            "action": "get",
            "value": None
            })
        logger.debug(f"value getted is {ans['value']}")
        return ans['value']

    def val_set(self, item, val):
        ans=self.inf.send({
            "section": "speaker",
            "item": item,
            "action": "set",
            "value": val 
            })
        if ans['value'] == val:
            logger.debug(f"value set to {val}")
        else:
            logger.error(f"value is not set to {val}")
        

    def chosen_file(self, obj, val):
        logger.debug(f"file chosen: {val}")
        self.open_file_dialog(None)
        ans=self.inf.send({
            "section": "speaker",
            "item": 'speaker.ini',
            "action": "set",
            "value": val
            })
        # wait for answer and update
        if ans['action'] == 'answer':
            self.update_all_gui()
        else:
            debug.error("can't update data from ini")

    def update_all_gui(self):
        print("update GUI values")
        self.speaker_producer.text = (self.val_get('producer'))
        self.speaker_model.text = (self.val_get('model'))
        for key, val in self.speaker_qts.items():
            print(key)
            val['value'].text = self.val_get(key)

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
    def open_file_dialog(self, event):
        logger.debug(f"key: open file pressed")
        if self.file_choose.disabled:
            self.file_choose.disabled = False
            self.file_choose.opacity=1
            self.name_all.size[1] += 200
            self.name_bottom.size[1] += 200
        else:
            self.file_choose.disabled = True
            self.file_choose.opacity=0
            self.name_all.size[1] -= 200
            self.name_bottom.size[1] -= 200



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

    def read_speaker_data():
        # send request for data
        ans=self.inf.send({
            "section": "speaker",
            "item": "list_quantities",
            "action": "get",
            "value": None,
            })
         
        for key, val in ans.items():
            logger.debug(key, val)

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
        ans=self.inf.send({
            "section": "speaker",
            "item": "producer",
            "action": "get",
            "value": None,
            })
        logcom.debug(f"answer from calc: {ans}")
        producer = ans['value']

        ans=self.inf.send({
            "section": "speaker",
            "item": "model",
            "action": "get",
            "value": None,
            })
        logcom.debug(f"answer from calc: {ans}")
        model = ans['value']


        self.name_all = BoxLayout(
                    orientation='vertical',
                    size=(500, HEIGHT),
                    size_hint = (1, None )
                    )
        name_top = BoxLayout(
                    orientation="horizontal",
                    size=(500, self.name_all.height),
                    size_hint = (1, None )
                    )
        self.name_bottom = BoxLayout(
                    orientation="horizontal",
                    size=(500, 0),
                    size_hint = (1, None )
                    )

        #speaker_producer = Label(text=str(self.producer))
        self.speaker_producer = Label(text=str(producer))
        self.speaker_model = Label(text=str(model))
        open_speaker_ini = Button(text="open file")
        open_speaker_ini.bind(on_press = self.open_file_dialog)
        name_top.add_widget(self.speaker_producer)
        name_top.add_widget(self.speaker_model)
        name_top.add_widget(open_speaker_ini)
        # TODO button and hide/unhide
        speaker_ini_path = os.path.join(os.getcwd(), "speakers")
        self.file_choose = FileChooserListView(
                path = speaker_ini_path,
                disabled = True,
                opacity=0
                )
        self.file_choose.bind(selection=self.chosen_file)
        self.name_bottom.add_widget(self.file_choose)
        self.name_all.add_widget(name_top)
        self.name_all.add_widget(self.name_bottom)
        speaker_layout.add_widget(self.name_all)
        # ask about all quantities for speaker
        ans=self.inf.send({
            "section": "speaker",
            "item": "list_quantities",
            "action": "get",
            "value": None,
            })
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
                        desc_btn = DescButton(btnsize = all_layout.height)
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
