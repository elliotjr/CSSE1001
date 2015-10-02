###################################################################
#
#   CSSE1001/7030 - Assignment 2
#
#   Student Number: 43569175
#
#   Student Name: Elliot Randall
#
###################################################################

#
# Do not change the following import
#

from assign2_support import *

####################################################################
#
# Insert your code below
#
####################################################################

class PVData(object):
    """Class to hold the PV data for a given date."""
    def __init__(self):
        """Constructs an instance of data."""
        self.dateStr = yesterday()
        self.dateStr = self.change_date(yesterday())
        self.arraydict = {}
                          

    def change_date(self, date): #re-initialize 
        if date != self.dateStr:
            self.dateStr = date
            self.data = load_data(self.dateStr)
            arraydict = {}
            for i, array in enumerate(ARRAYS):
                powers = []
                for row in self.data:
                    powers.append(row[3][i])
                arraydict[array] = powers   
            self.arraydict = arraydict
            self.temperature = []
            self.sunlight = []
            for i in self.data:
                self.temperature.append(i[1])
                self.sunlight.append(i[2])
            
    def get_date(self):
        return self.dateStr

    def get_time(self, time_index):
        timelist = []
        for i in self.data:
            timelist.append(i[0])
        return timelist[time_index]

    def get_temperature(self):
        return self.temperature     

    def get_sunlight(self):
        return self.sunlight

    def get_power(self, array):
        return self.arraydict.get(array, 0)
    

class Plotter(Canvas):
    """This class is responsible for doing the plotting on a canvas. Inherits from
    Canvas."""
    def __init__(self, master, controller):#PVData() initialized in data
        """Creates a plotter to draw on
        master - Top level window
        controller - the app object
        """
        
        self.height = 500
        self.width = 700
        Canvas.__init__(
            self, master, bg = "white", height = self.height,
            width = self.width, relief = SUNKEN, bd=2)
        self.controller = controller
        self.translator = CoordinateTranslator(
            self.width, self.height, len(self.controller.data.get_temperature()))
        self.bind("<Configure>", self.x_resize)
        self.frame = OptionsFrame(master, None)
        self.array = 'All Arrays Combined'


    def x_resize(self, event):
        """Re-plot data scaled to new window size on resize"""
        self.translator.resize(self.width, self.height)
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.translator = CoordinateTranslator(
            self.width, self.height, len(self.controller.data.get_temperature()))
        self.controller.update_plot()

          
    def draw_power(self):
        """Creates a line that plots the power as a polygon"""
        powerlist = []
        for index, power in enumerate(self.controller.data.get_power(self.array)):
            entry = self.translator.power_coords(index, power, self.array)
            powerlist.append(entry)
        self.create_polygon(powerlist, fill=POWER_COLOUR,
                            width=1, outline=POWER_COLOUR)
        
    def draw_temp(self):
        """Creates a line that plots the temperature as a line"""
        templist = []
        for index, temp in enumerate(self.controller.data.get_temperature()):
            entry = self.translator.temperature_coords(index, temp)
            templist.append(entry)
        self.create_line(templist, fill='red', width=1)

    def draw_sunlight(self):
        """Creates a line that plots the sunlight as a line"""
        sunlist = []
        for index, light in enumerate(self.controller.data.get_sunlight()):
            entry = self.translator.sunlight_coords(index, light)
            sunlist.append(entry)
        self.create_line(sunlist, fill='orange', width=1)

    def index(self, x):
        """Returns the x coordinate for a given index on a plot
        Returns None if goes past window to right"""
        x = self.translator.get_index(x)
        if x > len(self.controller.data.get_temperature())-1:
            return 
        else:
            self.time = self.controller.data.get_time(x)
            self.temperature = self.controller.data.get_temperature()[x]
            self.sunlight = self.controller.data.get_sunlight()[x]
            self.power = self.controller.data.get_power(self.array)[x]
        

    def draw_line(self, e, x, y):
        """Creates a vertical black line"""
        self.black = self.create_line(
            x, 0,
            x, self.height, fill='black', width=1)


class OptionsFrame(Frame):
    """This class is the'widget' used for choosing options and inherits
    from Frame."""
    def __init__(self, master, controller):
        """Creates the widget for user interaction
        master - Top level interface
        controller - the app object
        """
        
        Frame.__init__(self, master)
        
        self.tvar = BooleanVar()#Check Button Variables
        self.pvar = BooleanVar()
        self.svar = BooleanVar()
        
        self.checkFrame = Frame(self)
        self.checkFrame.pack(side=TOP)
        
        self.powerCheck = Checkbutton(
            self.checkFrame, text="Power",
            variable=self.pvar, command=self.check_update)
        self.powerCheck.pack(side=LEFT)
        self.tempCheck = Checkbutton(self.checkFrame, text="Temperature",
                                      variable = self.tvar,
                                      command=self.check_update)
        self.tempCheck.pack(side=LEFT)
        self.sunCheck = Checkbutton(
            self.checkFrame, text="Sunlight",
            variable=self.svar, command=self.check_update)
        self.sunCheck.pack(side=LEFT)
        self.pvar.set(True)

        
        self.controller = controller
        self.entryFrame = Frame(self)
        self.entryFrame.pack(side=LEFT, anchor = W)
        self.ChooseDate = Label(self.entryFrame, text="Choose Date:")
        self.ChooseDate.pack(side=LEFT, padx=5)
        self.entry = Entry(self.entryFrame, width=20)
        self.entry.pack(side=LEFT, padx=5)
        #This is the apply button - click it to show the graph
        self.apply = Button(self.entryFrame, text="Apply",
                             command=self.change1)
        self.apply.pack(side=LEFT, padx=5, pady = 10)

        arrays = ARRAYS[-1]
        self.Position = StringVar()
        self.Position.set(arrays)

        self.alist = OptionMenu(
            self, self.Position, *ARRAYS, command=self.change_building1)
        self.alist.pack(side=RIGHT, anchor = E, fill=X, pady = 10, padx=5)     
        #self._Position holds the building name - send to coordinates
        
    def change_building1(self, event):
        """changes the building selected in option menu"""
        new_array = self.Position.get()
        self.controller.change_array(new_array)

    def check_update(self):
        """Checks the state of update buttons"""
        self.controller.update_plot()        

    def change1(self):
        """Calls method to change date"""
        entry = self.entry.get()
        try:
            self.content = entry
            self.controller.change_date(self.content)
        except ValueError as error:
            tkMessageBox.showerror("Date Error", error.message)

class LabelFrame(Frame):
    """This class is the Frame at the top which holds the label for
    displaying time, tem, date, sunlight etc.
    """
    def __init__(self, master, controller):
        """Creates the label at top of window
        master - top level window
        controller - the app object
        """
        self.controller = controller
        Frame.__init__(self, master)
        self.printed = None
        self.prettyPrint = Label(self, text=self.printed)
        self.prettyPrint.pack(side=LEFT, pady=5)


class PVPlotApp(object):
    """
    This is the top level class for the GUI. It is responsible for creating and
    managing instances of the above classes. 
    """
    def __init__(self, master):
        """Creates a class that holds instances of other classes
        master = top level window
        """
        master.title("PV Plotter App")
        self.master = master
        self.LabelWidget = LabelFrame(master, self)
        self.LabelWidget.pack(fill=X, side=TOP)
        self.data = PVData()
        self.data.change_date(yesterday())
        self.canvas = Plotter(master, self)
        self.canvas.pack(fill=X, expand=True, padx=10)
        self.widget = OptionsFrame(master, self)
        self.widget.pack(fill=X, anchor=E, expand=True)
        self.update_plot()
        self.canvas.bind("<Button-1>", self.ButtonPress)
        self.canvas.bind("<Motion>", self.ButtonMotion)
        self.canvas.bind("<ButtonRelease-1>", self.ButtonRelease)
        self.clicked = False
        self.yesterday = self.data.get_date()
        self.widget.entry.insert(0, self.yesterday)
        master.minsize(600, 400)
        
    def ButtonPress(self, event):
        """Event handler for when the Left mouse button has been clicked"""
        self.clicked = True
        self.update_plot()
        self.newx = event.x
        self.newy = event.y
        self.canvas.draw_line(None, self.newx, self.newy)
        self.canvas.index(self.newx)#for the black line
        self.create_ppdata()
        self.update_label()

        
    def ButtonMotion(self, event):
        """Draws the line in the new position"""
        if self.clicked == True: 
            self.update_plot()
            self.newx = event.x
            self.newy = event.y
            self.canvas.draw_line(None, self.newx, self.newy)
            self.canvas.index(self.newx)#for the black line
            self.create_ppdata()
            self.update_label()
        else:
            return      

    def ButtonRelease(self, e):
        """Event handler for when the left mouse has been released"""
        self.canvas.delete(ALL)
        self.update_plot()
        self.clicked = False

    def update_plot(self):
        self.canvas.delete(ALL)
        if self.widget.pvar.get() == True:
            self.canvas.draw_power()
        if self.widget.tvar.get() == True:
            self.canvas.draw_temp()
        if self.widget.svar.get() == True:
            self.canvas.draw_sunlight()
        self.LabelWidget.prettyPrint.config(
            text='Data for {0}'.format(self.data.get_date()))
        #update plot when apply is pressed
        #OptionsFrame -> tell PVPapp when options frame is pressed

    def change_date(self, dateStr):
        self.data.change_date(dateStr)
        self.update_plot()
    
    def change_array(self, array):
        self.canvas.delete(ALL)
        self.canvas._array = array
        self.update_plot()

    def create_ppdata(self):
        if self.widget.pvar.get() == False:
            power = None
        else: 
            power = self.canvas.power
            
        if self.widget.tvar.get() == False:
            temp = None
        else: 
            temp = self.canvas.temperature

        if self.widget.svar.get() == False:
            sun = None
        else: 
            sun = self.canvas.sunlight
            
        time = self.canvas.time
        date = self.data.get_date()
        self.pp = pretty_print_data(date, time, temp, sun, power, is_cumulative=False)

    def update_label(self):
        self.LabelWidget.prettyPrint.config(
            text= self.pp)
    
         
        
#24/09/2014 Plotter initialized with PV data.
#25/09/2014 Plotter Gui has been installed. 
#26/09/2014 Unpacked Arrays * - (Pointer).
#03/10/2014 Added Draw temp/sunlight on click - power added as well.
#06/10/2014 Added resize on click - config. - resize works.
#07/10/2014 The graph now changes.
#07/10/2014 There is a little problem - resize.
#07/10/2014 Changing Power Array Works!
#08/10/2014 The resize Method is working - update_plot.
        #called from PVPData() on resize.
#08/10/2014 The checkbuttons have full functionality.
#08/10/2014 Blackline is appearing when click and disapear on release -
        #no movement.
#09/10/2014 The black line movement has been completed.
#09/10/2014 Get_index method has been implemented in Plotter class.
#10/10/2014 Pretty Print has been implemented - index range error fix. 


        

####################################################################
#
# WARNING: Leave the following code at the end of your code
#
# DO NOT CHANGE ANYTHING BELOW
#
####################################################################

def main():
    root = Tk()
    app = PVPlotApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()

