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
        self._dateStr = None 
        self._dateStr = self.change_date(yesterday())
        self._arraydict = {}
                          
    def change_date(self, date): #re-initialize 
        if date != self._dateStr:
            self._dateStr = date
            self._data = load_data(self._dateStr)
            arraydict = {}
            for i, array in enumerate(ARRAYS):
                powers = []
                for row in self._data:
                    powers.append(row[3][i])
                arraydict[array] = powers   
            self._arraydict = arraydict
            self._temperature = []
            self._sunlight = []
            for i in self._data:
                self._temperature.append(i[1])
                self._sunlight.append(i[2])
            
    def get_date(self):
        return self._dateStr

    def get_time(self, time_index):
        timelist = []
        for i in self._data:
            timelist.append(i[0])
        return timelist[time_index]

    def get_temperature(self):
        return self._temperature     

    def get_sunlight(self):
        return self._sunlight

    def get_power(self, array):
        return self._arraydict.get(array, 0)
    

class Plotter(Canvas):
    """This class is responsible for doing the plotting on a canvas. Inherits from
    Canvas."""
    def __init__(self, master, controller):#PVData() initialized in data
        """Creates a plotter to draw on
        master - Top level window
        controller - the app object
        """       
        self.height = 600
        self.width = 800
        Canvas.__init__(
            self, master, bg = "white", height = self.height,
            width = self.width, relief = SUNKEN, bd=2)
        self.data = PVData()
        self.data.change_date(yesterday())
        self._translator = CoordinateTranslator(
            self.width, self.height, len(self.data.get_temperature()))
        self.bind("<Configure>", self.x_resize)
        self.frame = OptionsFrame(master, None)
        self._array = 'All Arrays Combined'
        self._controller = controller

    def x_resize(self, event):
        """Re-plot data scaled to new window size on resize"""
        self._translator.resize(self.width, self.height)
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self._translator = CoordinateTranslator(
            self.width, self.height, len(self.data.get_temperature()))
        self._controller.update_plot()
          
    def draw_power(self):
        """Creates a line that plots the power as a polygon"""
        powerlist = []
        for index, power in enumerate(self.data.get_power(self._array)):
            entry = self._translator.power_coords(index, power, self._array)
            powerlist.append(entry)
        self.create_polygon(powerlist, fill=POWER_COLOUR,
                            width=1, outline=POWER_COLOUR)
        
    def draw_temp(self):
        """Creates a line that plots the temperature as a line"""
        templist = []
        for index, temp in enumerate(self.data.get_temperature()):
            entry = self._translator.temperature_coords(index, temp)
            templist.append(entry)
        self.create_line(templist, fill='red', width=1)

    def draw_sunlight(self):
        """Creates a line that plots the sunlight as a line"""
        sunlist = []
        for index, light in enumerate(self.data.get_sunlight()):
            entry = self._translator.sunlight_coords(index, light)
            sunlist.append(entry)
        self.create_line(sunlist, fill='orange', width=1)

    def index(self, x):
        """Returns the x coordinate for a given index on a plot
        Returns None if goes past window to right"""
        x = self._translator.get_index(x)
        if x > len(self.data.get_temperature())-1:
            return 
        else:
            self.time = self.data.get_time(x)
            self.temperature = self.data.get_temperature()[x]
            self.sunlight = self.data.get_sunlight()[x]
            self.power = self.data.get_power(self._array)[x]
        

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
        self._checkFrame = Frame(self)
        self._checkFrame.pack(side=TOP, expand=True)       
        self._powerCheck = Checkbutton(
            self._checkFrame, text="Power",
            variable=self.pvar, command=self.check_update)
        self._powerCheck.pack(side=LEFT, expand=True)
        self._tempCheck = Checkbutton(self._checkFrame, text="Temperature",
                                      variable = self.tvar,
                                      command=self.check_update)
        self._tempCheck.pack(side=LEFT)
        self._sunCheck = Checkbutton(
            self._checkFrame, text="Sunlight",
            variable=self.svar, command=self.check_update)
        self._sunCheck.pack(side=LEFT)
        self.pvar.set(True)        
        self._controller = controller
        self._entryFrame = Frame(self)
        self._entryFrame.pack(side=LEFT, anchor = W)
        self._ChooseDate = Label(self._entryFrame, text="Choose Date:")
        self._ChooseDate.pack(side=LEFT, padx=5)
        self._entry = Entry(self._entryFrame, width=20)
        self._entry.pack(side=LEFT, padx=5)
        #This is the apply button - click it to show the graph
        self._apply = Button(self._entryFrame, text="Apply",
                             command=self.change1)
        self._apply.pack(side=LEFT, padx=5, pady = 10)
        arrays = ARRAYS[-1]
        self._Position = StringVar()
        self._Position.set(arrays)
        self._alist = OptionMenu(
            self, self._Position, *ARRAYS, command=self.change_building1)
        self._alist.pack(side=RIGHT, anchor = E, fill=X, pady = 10, padx=5)     
        #self._Position holds the building name - send to coordinates
        
    def change_building1(self, event):
        """changes the building selected in option menu"""
        new_array = self._Position.get()
        self._controller.change_array(new_array)

    def check_update(self):
        """Checks the state of update buttons"""
        self._controller.update_plot()        

    def change1(self):
        """Calls method to change date"""
        entry = self._entry.get()
        try:
            self._content = entry
            self._controller.change_date(self._content)
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
        self._controller = controller
        Frame.__init__(self, master)
        self.printed = None
        self._prettyPrint = Label(self, text=self.printed)
        self._prettyPrint.pack(side=LEFT, pady=5)


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
        self._master = master
        #Create an instance of the (Model) 
        #Create the Options menu (View)
        self._LabelWidget = LabelFrame(master, self)
        self._LabelWidget.pack(fill=BOTH, side=TOP, expand=True)
        #Create the canvas (View)
        self._canvas = Plotter(master, self)
        self._canvas.pack(fill=BOTH, expand=True, padx=10)
        self._widget = OptionsFrame(master, self)
        self._widget.pack(fill=BOTH, expand=True, anchor=S)
        self.update_plot()
        self._canvas.bind("<Button-1>", self.ButtonPress)
        self._canvas.bind("<Motion>", self.ButtonMotion)
        self._canvas.bind("<ButtonRelease-1>", self.ButtonRelease)
        self.clicked = False #Whether Button1 has been clicked
        self.yesterday = self._canvas.data.get_date()
        self._widget._entry.insert(0, self.yesterday)
        master.minsize(600, 650)
        
    def ButtonPress(self, event):
        """Event handler for when the Left mouse button has been clicked"""
        self.clicked = True
        self.update_plot()
        self.newx = event.x
        self.newy = event.y
        self._canvas.draw_line(None, self.newx, self.newy)
        self._canvas.index(self.newx)#for the black line
        self.create_ppdata()
        self.update_label()

        
    def ButtonMotion(self, event):
        """Draws the line in the new position"""
        if self.clicked == True: 
            self.update_plot()
            self.newx = event.x
            self.newy = event.y
            self._canvas.draw_line(None, self.newx, self.newy)
            self._canvas.index(self.newx)#for the black line
            self.create_ppdata()
            self.update_label()
        else:
            return      

    def ButtonRelease(self, e):
        """Event handler for when the left mouse has been released"""
        self._canvas.delete(ALL)
        self.update_plot()
        self.clicked = False

    def update_plot(self):
        """Updates the lines/polygons on the canvas"""
        self._canvas.delete(ALL)
        if self._widget.pvar.get() == True:
            self._canvas.draw_power()
        if self._widget.tvar.get() == True:
            self._canvas.draw_temp()
        if self._widget.svar.get() == True:
            self._canvas.draw_sunlight()
        self._LabelWidget._prettyPrint.config(
            text='Data for {0}'.format(self._canvas.data.get_date()))

    def change_date(self, dateStr):
        """Changes the date for data in order to update the plot"""
        self._canvas.data.change_date(dateStr)
        self.update_plot()
    
    def change_array(self, array):
        """Changes the data when a different array is displayed"""
        self._canvas.delete(ALL)
        self._canvas._array = array
        self.update_plot()

    def create_ppdata(self):
        """Creates input for pretty print"""
        if self._widget.pvar.get() == False:
            power = None
        else: 
            power = self._canvas.power
            
        if self._widget.tvar.get() == False:
            temp = None
        else: 
            temp = self._canvas.temperature

        if self._widget.svar.get() == False:
            sun = None
        else: 
            sun = self._canvas.sunlight
            
        time = self._canvas.time
        date = self._canvas.data.get_date()
        self.pp = pretty_print_data(date, time, temp, sun, power, is_cumulative=False)

    def update_label(self):
        """Updates the pretty print label at the top of page"""
        self._LabelWidget._prettyPrint.config(
            text= self.pp)
        

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

