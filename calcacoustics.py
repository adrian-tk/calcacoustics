#! env/bin/python

# TODO move function to files 
# import logging stuff at first

try:
    from solver.logger import logging 
    from solver.logger import logger
    from solver.logger import logcom
    from solver.logger import loggui
    logger.debug("imported loggers")
    from solver.logger import setlog
    from solver.logger import list_log
    #setlog('debug')
    #setlog('com')
    #setlog('all')
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
from kivy.uix.scrollview import ScrollView
from kivy.metrics import sp

import interface
from gui_kivy.kivy_common import FloatInput
from gui_kivy.kivy_common import DescButton

# print available loggers
list_log()

logger.debug(f"platform is {platform}")

class Comm():
    """class to communicate with interface"""
    # create interface
    def __init__(self, name:str = "default"):
        self.name = name
        self.inf=interface.Interface()

    def getval(self, item: str) -> str:
        """prepare query for interface, and return value

        Example:
        >>> getval('fs')
        "6.0"

        Args:
            item: quantity to get value

        Return:
            value of item quantity
        """
        # query for sending to interface
        query = {
            "section": self.name,
            "item": item,
            "action": "get",
            "value": "",
            }
        logcom.debug(f"comm sent to interface: {query}")
        ans=self.inf.ask(query)
        logcom.debug(f"comm get from interface: {ans}")
        logger.debug(
                f"getting {self.name}: {item} and get {ans[0]['value']}"
                )
        # TODO get better list working? or maybe the first one is ok?
        return(ans[0]["value"])

    def setval(self, item: str, val: str) -> list:
        """query for setting value in solver

        Example:
        >>> setval('fs', '3.0')
        <list of quantities>

        Args:
            item: quantity to set
            val: value to set

        Return:
            list of dictionaries, first dic is confirmation,
            next are with updated values
        """
        query = {
            "section": self.name,
            "item": item,
            "action": "set",
            "value": val
            }
        logcom.debug(f"comm sent to interface: {query}")
        ans=self.inf.ask(query)
        logcom.debug(f"comm get from interface: {ans}")
        logger.debug(f"setting {self.name}: {item} with {val} updated")
        return(ans)

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

    def getsections(self):
        """returns data to populate GUI"""
        query = {
            "section": self.name,
            "item": "list_sections",
            "action": "get",
            "value": None,
            }
        logcom.debug(f"send to interface: {query}")
        ans=self.inf.ask(query)
        logcom.debug(f"get from interface: {ans}")
        logger.debug(f"list of sections {self.name} queried")
        return(ans[0]['value'])

    def getlist(self):
        """returns data to populate GUI"""
        query = {
            "section": self.name,
            "item": "list_quantities",
            "action": "get",
            "value": None,
            }
        logcom.debug(f"send to interface: {query}")
        ans=self.inf.ask(query)
        logcom.debug(f"get from interface: {ans}")
        logger.debug(f"dictionary for populate {self.name} queried")
        return(ans[0]['value'])

class QuantBundle():
    """class for creating and working with multiple data widgets
    
    object of this class shall be self. in def build()
    to dispatch (ie. clicking) working

    widgets in this class:
        header: TODO
            name
            description 
            save to file
            read from file
        data bundle:
            names
            names
        drawing TODO
    """
    def __init__(self, name:str="", comm:Comm=None):
        self.HEIGHT = sp(30)
        # use existing com if sent as parameter
        # if not, create a new one using name
        self.bundle_name = name
        if comm is None:
            self.comm = Comm(self.bundle_name)
        else:
            self.comm = comm
        #self.dictionary = self.comm.populate()
        self.dictionary = self.comm.getlist()
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
        self.data_name = Label(text="default name")
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
            logger.debug(f"ini path: {bundle_ini_path}")
            ini_file = bundle_ini_path + "test.ini"
            with open(ini_file, 'w') as f:
                f.write('test')
        else:
            #bundle_ini_path = os.path.join(os.getcwd(), "speakers")
            bundle_ini_path = os.path.join(
                    os.getcwd(),
                    'input',
                    self.bundle_name,
                    )
            logger.debug(f"ini path: {bundle_ini_path}")
        self.file_choose = FileChooserListView(
                path = bundle_ini_path,
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

        ans=self.comm.setval("file.ini", val)
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

                    case 'dependencies':
                        # don't show this
                        pass
                                
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
        self.data_name.text = (self.comm.getval('name'))
        for key, val in self.data_qts.items():
            ans = self.comm.getval(key)
            val['value'].text = str(ans)

    def calc_update(self):
        logger.debug("recalculate EBP")
        ans = self.comm.cal("EBP")
        self.data_qts["EBP"]["value"].text=str(ans)

    def num_val_update(self, instance, value):
        """ triggered after putting numbers in input field"""
        # for some reason, when replacing value, empty string is
        # sending firs, this "if" shall reject it.
        if value != "":
            logger.debug(
                    f"value: {value}, key: {instance.kname} updated in GUI"
                    )
            answers = self.comm.setval(instance.kname, value)
            for answer in answers:
                if answer["action"] == "answer":
                    self.data_qts[answer['item']]["value"].text= \
                            str(answer['value'])
                    logger.debug(f"{answer['item']} updated")


class CalcAcousticsApp(App):

    def windows_size(self, *args):
        xwin = self.root.size[0]
        ywin = self.root.size[1]
        xywin = (xwin, ywin)
        for section in self.section_list:
            self.scroll_views[section].size = xywin
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

        accordion type
        """
        Window.bind(on_resize=self.windows_size)
        self.root=Accordion()
        if platform == 'android':
            self.root.orientation='vertical'
        # # generate sections
        #
        c = Comm("interface")
        #self.section_list = ['speaker']
        self.section_list = c.getsections()
        # dictionary for objects
        self.bundles = {}
        self.items = {}
        self.scroll_views = {}
        for section in self.section_list:
            self.items[section]=AccordionItem(title=section)
            self.scroll_views[section] = ScrollView(
                    size_hint=(1, None),
                    size=(Window.width, Window.height),
                    scroll_timeout=1,
                    scroll_type=['bars'],
                    bar_width=sp(20)

                    )
            x_layout=BoxLayout(orientation="vertical")
            x_layout.size_hint_y = None
            x_layout.bind(minimum_height=x_layout.setter('height'))
            self.bundles[section] = QuantBundle(section)
            header = self.bundles[section].populate_header()
            x_layout.add_widget(header)
            widget = self.bundles[section].populate_with_dicts()
            x_layout.add_widget(widget)
            #x_layout.add_widget(Label(text="END"))
            self.scroll_views[section].add_widget(x_layout)
            self.items[section].add_widget(self.scroll_views[section])
            self.root.add_widget(self.items[section])
        # open speaker item as default when running program
        self.items['speaker'].collapse=False
        self.windows_size()
        return self.root
if __name__=="__main__":
    CalcAcousticsApp().run()

