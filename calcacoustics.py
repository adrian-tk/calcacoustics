#! env/bin/python

# import logging stuff at first
# TODO move function for files 

try:
    from solver.logger import logging 
    from solver.logger import logger
    from solver.logger import logcom
    from solver.logger import loggui
    logger.debug("imported loggers")
    from solver.logger import setlog
    #setlog('debug')
    setlog('all')
except Exception as err:
    print("Can't import loggers")
    print(err)
    print("maybe You shold be in env?")

import os
from kivy.core.window import Window
from kivy.utils import platform
if platform == 'android':
    from android import mActivity
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.metrics import sp

import interface
from gui_kivy.kivy_common import FloatInput
from gui_kivy.kivy_common import DescButton

# print available loggers
loggers = [logging.getLogger(name) for name in \
        logging.root.manager.loggerDict]
for logg in loggers:
    logger.debug(logg)

logger.debug(f"platform is {platform}")

class Comm():
    """class to communicate with interface"""
    # create interface
    def __init__(self, name:str = "default"):
        self.name = name
        self.inf=interface.Interface()

    def get(self, item: str) -> str:
        query = {
            "section": self.name,
            "item": item,
            "action": "get",
            "value": "",
            }
        logcom.debug(f"sending to interface: {query}")
        ans=self.inf.send(query)
        logcom.debug(f"get from interface: {ans}")
        logger.debug(
                f"getting {self.name}: {item} and get {ans['value']}"
                )
        return(ans["value"])

    def set(self, item: str, val: str) -> bool:
        query = {
            "section": self.name,
            "item": item,
            "action": "set",
            "value": val
            }
        logcom.debug(f"sending to interface: {query}")
        ans=self.inf.send(query)
        logcom.debug(f"get from interface: {ans}")
        logger.debug(f"setting {self.name}: {item} with {val} updated")
        # for checking correction if needed
        return(True)

    def cal(self, item: str) -> str:
        query = {
            "section": self.name,
            "item": item,
            "action": "calculate",
            "value": ""
            }
        logcom.debug(f"send to interface: {query}")
        ans=self.inf.send(query)
        logcom.debug(f"get from interface: {ans}")
        logger.debug(f"calculate {self.name}: {item}")
        return(ans["value"])

    def populate(self):
        """returns data to populate GUI"""
        query = {
            "section": self.name,
            "item": "list_quantities",
            "action": "get",
            "value": None,
            }
        logcom.debug(f"send to interface: {query}")
        ans=self.inf.send(query)
        logcom.debug(f"get from interface: {ans}")
        logger.debug(f"dictionary for populate {self.name} queried")
        return(ans)

class QuantBundle():
    """class for creating and working with multiple data widgets
    
    object of this class shall be self. in def build()
    to dispatch (ie. clicking) working

    widgets in this class:
        header: TODO
            name
            save to file
            read from file
        data bundle:
            names
            names
        drawing TODO
    """
    def __init__(self, name:str="", comm:Comm=None):
        self.HEIGHT = sp(30)
        self.bundle_name = name
        if comm is None:
            self.comm = Comm(self.bundle_name)
        else:
            self.comm = comm
        self.dictionary = self.comm.populate()
        # dictionary of dictionaries to hold
        # data from widget created in loop
        # ie: {Qts: {unit: <some object>}}
        self.data_qts={}
        #self.inf=interface.Interface()
        logger.debug(
                f'Quant object with name: "{self.bundle_name}" created'
                )

    def open_description(self, event):
        for key, val in self.data_qts.items():
            if val['desc_btn'] == event:
                #print (self.speaker_qts[key])
                logger.debug(f"key: {key} pressed")
                a=self.data_qts[key]
                if a['desc_label'].disabled:
                    a['bottom_layout'].size[1] = '70sp'
                    a['big_layout'].size[1] = '100sp'
                    a['desc_label'].opacity=1
                    a['desc_label'].disabled=False
                    a['desc_label'].size = a['bottom_layout'].size
                    a['desc_label'].text_size = a['desc_label'].size
                    #print(a['desc_label'].text_size)
                    self.main_layout.size[1] += sp(70)
                else:
                    a['bottom_layout'].size=(500,0 )
                    a['big_layout'].size=(500, self.HEIGHT)
                    a['desc_label'].opacity=0
                    a['desc_label'].disabled=True
                    self.main_layout.size[1] -= sp(70)

    def populate_header(self):
        """
        header_main:
            header_top:
                name
                save
                read
            header_bottom:
                <place for additional data, default hide>
        """
        #self.name_all = BoxLayout(
        self.header_main = BoxLayout(
                    orientation='vertical',
                    size=(500, self.HEIGHT),
                    size_hint = (1, None )
                    )
        self.header_top = BoxLayout(
                    orientation="horizontal",
                    size=(500, self.header_main.height),
                    size_hint = (1, None )
                    )
        self.header_bottom = BoxLayout(
                    orientation="horizontal",
                    size=(500, 0),
                    size_hint = (1, None )
                    )
        self.data_name = Label(text="coded in name")
        open_ini = Button(text="open file")
        open_ini.bind(on_press = self.open_file_dialog)
        self.header_top.add_widget(self.data_name)
        self.header_top.add_widget(open_ini)
        if platform == 'android':
            context = mActivity.getApplicationContext()
            result = context.getExternalFilesDir(None)
            if result:
                bundle_ini_path = str(result.toString())
            else:
                bundle_ini_path = app_storage_path()
            logger.debug(f"ini path: {speaker_ini_path}")
            ini_file = bundle_ini_path + "test.ini"
            with open(ini_file, 'w') as f:
                f.write('test')
        else:
            speaker_ini_path = os.path.join(os.getcwd(), "speakers")
            logger.debug(f"ini path: {speaker_ini_path}")
        self.file_choose = FileChooserListView(
                path = speaker_ini_path,
                disabled = True,
                opacity=0
                )
        self.file_choose.bind(selection=self.chosen_file)
        self.header_bottom.add_widget(self.file_choose)
        self.header_main.add_widget(self.header_top)
        self.header_main.add_widget(self.header_bottom)
        return(self.header_main)
        #speaker_layout.add_widget(self.name_all)

    def open_file_dialog(self, event):
        widget_height = 200
        logger.debug(f"key: open file pressed")
        if self.file_choose.disabled:
            self.file_choose.disabled = False
            self.file_choose.opacity=1
            self.header_main.size[1] += sp(widget_height)
            self.header_bottom.size[1] += sp(widget_height)
            #self.tmpans.text=self.file_choose.path
        else:
            self.file_choose.disabled = True
            self.file_choose.opacity=0
            self.header_main.size[1] -= sp(widget_height)
            self.header_bottom.size[1] -= sp(widget_height)

    def chosen_file(self, obj, val):
        logger.debug(f"file chosen: {val}")
        self.open_file_dialog(None)

        ans=self.comm.set("speaker.ini", val)
        # wait for answer and update
        if ans:
            self.update_all_gui()
        else:
            debug.error("can't update data from ini")

    def populate_with_dicts(self):
        """populate widget with data from dictionary

        main_layout:
            big_layout:
                top_layout:
                bottom_layout:
            big_layout:
                top_layout:
                bottom_layout:
            ...
        """
        # main layout
        self.main_layout=BoxLayout(
                orientation="vertical",
                size=(500, 0),
                size_hint = (1, None),
                )
        # outside loop for get quantity
        for key, val in self.dictionary.items():
            # dict for widgets in quantity
            qty_widgets={}
            # BoxLayout for quantity
            # top: name, short name, value, unit etc.
            # bottom to hide with help, and lock
            big_layout = BoxLayout(
                    orientation='vertical',
                    size=(500, self.HEIGHT),
                    size_hint = (1, None )
                    )
            loggui.debug(f"big_layout size: {big_layout.size}")
            loggui.debug(f"big_layout size_hint: {big_layout.size_hint}")
            top_layout = BoxLayout(
                    orientation="horizontal",
                    size=(500, big_layout.height),
                    size_hint = (1, None )
                    )
            loggui.debug(f"top_layout size: {top_layout.size}")
            loggui.debug(f"top_layout size_hint: {top_layout.size_hint}")
            bottom_layout = BoxLayout(
                    orientation="horizontal",
                    size=(500, 0),
                    size_hint = (1, None )
                    )
            loggui.debug(f"bottom_layout size: {bottom_layout.size}")
            loggui.debug(f"bottom_layout size_hint: {bottom_layout.size_hint}")
            qty_widgets.update({
                    'big_layout': big_layout,
                    'top_layout': top_layout,
                    'bottom_layout': bottom_layout
                    })
            # internal loop for populate each quantity
            for ikey, ival in self.dictionary[key].items():
                match ikey:
                    case "desc":
                        desc_btn = DescButton(btnsize = big_layout.height)
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
                            size_hint = (None, 1),
                            size = ('80sp', 0)
                            )
                        qty_val.kname = key
                        qty_val.bind(text=self.num_val_update)
                        top_layout.add_widget(qty_val)

                        qty_widgets.update({
                            'value': qty_val,
                            })
                                
                    case default:
                        tmp_q = Label(text=str(ival))
                        if ikey == 'unit':
                            tmp_q.size_hint = (None, 0.5)
                        if ikey == 'short_name':
                            tmp_q.size_hint = (None, 0.5)
                        top_layout.add_widget(tmp_q)

                        qty_widgets.update({
                            ikey: tmp_q,
                            })


            self.data_qts.update({key: qty_widgets})
            big_layout.add_widget(top_layout)
            big_layout.add_widget(bottom_layout)
            self.main_layout.add_widget(big_layout)
            self.main_layout.height=self.main_layout.height+self.HEIGHT
            loggui.debug(f"main_layout size: {self.main_layout.size}")
            loggui.debug(f"main_layout size_hint: {self.main_layout.size_hint}")
        #logger.debug(self.data_qts)
        loggui.debug(
                f"main layout otuside loops is {self.main_layout.size}"
                )
        #with main_layout.canvas:
        #    Color(1, 0, 0)
        #    Rectangle(pos=main_layout.pos, size=main_layout.size)
        return(self.main_layout)

    def update_all_gui(self):
        # TODO fix it to class
        print("update GUI values")
        self.data_name.text = (self.comm.get('name'))
        #for key, val in self.speaker_qts.items():
        # TODO move to QuantBundle?
        for key, val in self.data_qts.items():
            ans = self.comm.get(key)
            print(f"key: {ans} updated")
            val['value'].text = ans

    def calc_update(self):
        logger.debug("recalculate EBP")
        ans = self.comm.cal("EBP")
        self.data_qts["EBP"]["value"].text=str(ans)

    def num_val_update(self, instance, value):
        """ triggered after putting numbers in input field"""

        logger.debug(f"value: {value}, key: {instance.kname} updated in GUI")
        ans = self.comm.set(instance.kname, value)
        self.calc_update()


class CalcAcousticsApp(App):

    def chosen_file(self, obj, val):
        logger.debug(f"file chosen: {val}")
        self.open_file_dialog(None)
        """
        ans=self.inf.send({
            "section": "speaker",
            "item": 'speaker.ini',
            "action": "set",
            "value": val
            })
            """
        ans=self.speaker_bundle.comm.set("speaker.ini", val)
        # wait for answer and update
        if ans:
            self.update_all_gui()
        else:
            debug.error("can't update data from ini")

    def update_all_gui(self):
        print("update GUI values")
        self.speaker_producer.text = (self.comm.get('producer'))
        self.speaker_model.text = (self.comm.get('model'))
        #for key, val in self.speaker_qts.items():
        # TODO move to QuantBundle?
        for key, val in self.speaker_bundle.data_qts.items():
            print(key)
            print(val['value'].text)
            print(f"key: {self.speaker_bundle.comm.get(key)}")
            val['value'].text = self.speaker_bundle.comm.get(key)
            #val['value'].text = self.speaker_get(key)
            val['value'].text = self.speaker_bundle.comm.get(key)

    def open_file_dialog(self, event):
        logger.debug(f"key: open file pressed")
        if self.file_choose.disabled:
            self.file_choose.disabled = False
            self.file_choose.opacity=1

            self.name_all.size[1] += sp(200)
            self.name_bottom.size[1] += sp(200)
            self.tmpans.text=self.file_choose.path
        else:
            self.file_choose.disabled = True
            self.file_choose.opacity=0
            self.name_all.size[1] -= sp(200)
            self.name_bottom.size[1] -= sp(200)

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

    def windows_size(self, *args):
        if platform == 'android':
            if self.root.size[0] > self.root.size[1]:
                self.root.orientation='vertical'
            else:
                self.root.orientation='horizontal'
        else:
            if self.root.size[0] < self.root.size[1]:
                self.root.orientation='vertical'
            else:
                self.root.orientation='horizontal'

    def build(self):
        """ buld views of GUI

        accrodion type
        """
        Window.bind(on_resize=self.windows_size)
        self.root=Accordion()
        if platform == 'android':
            self.root.orientation='veritcal'
        self.comm = Comm("speaker")
        self.inf=interface.Interface()
        #
        # Speaker
        #
        speaker_item=AccordionItem(title="Speaker")
        speaker_layout=BoxLayout(orientation="vertical")
        self.speaker_bundle = QuantBundle("speaker")
        header = self.speaker_bundle.populate_header()
        speaker_layout.add_widget(header)
        widget = self.speaker_bundle.populate_with_dicts()
        speaker_layout.add_widget(widget)
        self.tmpans = Label(text="END")
        speaker_layout.add_widget(self.tmpans)
        speaker_item.add_widget(speaker_layout)
        self.root.add_widget(speaker_item)
        #
        #Enclosure
        #
        enclosure_item=AccordionItem(title="Enclosure")
        enclosure_layout=BoxLayout(orientation="vertical")
        #self.bundle = QuantBundle("speaker")
        #widget = self.bundle.populate_with_dicts()
        #enclosure_layout.add_widget(widget)
        enclosure_layout.add_widget(Label(text="END"))
        enclosure_item.add_widget(enclosure_layout)
        self.root.add_widget(enclosure_item)
        # open speaker item as default when running program
        speaker_item.collapse=False
        self.windows_size()
        return self.root

if __name__=="__main__":
    CalcAcousticsApp().run()
