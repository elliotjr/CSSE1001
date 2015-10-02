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
        """Constructs an instance of data

        Constructor: PVData()
        
        PVData.__init__() -> None
        """
        self.dateStr = yesterday()
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
                          

    def change_date(self, date):
        """Creates data when date is changed

        Pre-Condition: Date entered is in dd-mm-yyyy format

        PVData.change_date(string) -> None
        """
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
        """Returns date for loaded data

        PVData.get_date(None) -> string
        """
        return self.dateStr

    def get_time(self, time_index):
        """Returns time at a given index

        PVData.get_date(int) -> string
        """
        timelist = []
        for i in self.data:
            timelist.append(i[0])
        return timelist[time_index]

    def get_temperature(self):
        """Returns temperature for data

        PVData.get_date(None) -> list
        """
        return self.temperature     

    def get_sunlight(self):
        """Returns sunlight for data

        PVData.get_date(None) -> list
        """
        return self.sunlight

    def get_power(self, array):
        """Returns power for given array

        PVData.get_date(string) -> list
        """
        return self.arraydict.get(array, 0)
    

class Plotter(Canvas):
    """This class is responsible for doing the plotting on a canvas.
    Inherits from canvas.
    """
    def __init__(self, master, controller):
        """Creates a plotter to draw on
        master - Top level window
        controller - the app object

        Plotter.__init__(TkClass, Class) -> None
        """
        
        self.height = master.winfo_height()
        self.width = master.winfo_width()
        Canvas.__init__(
            self, master, bg = "white", relief = SUNKEN, bd=2)
        self.controller = controller
        self.translator = CoordinateTranslator(
            master.winfo_width(), master.winfo_height(),
            len(self.controller.data.get_temperature()))
        self.bind("<Configure>", self.x_resize)
        self.frame = OptionsFrame(master, None)
        self.array = 'All Arrays Combined'

    def x_resize(self, event):
        """Re-plot data scaled to new window size on resize

        Plotter.x_resize(event) -> None
        """
        self.translator.resize(self.width, self.height)
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.translator = CoordinateTranslator(
            self.width, self.height, len(
                self.controller.data.get_temperature()))
        self.controller.update_plot()

          
    def draw_power(self):
        """Creates a line that plots the power as a polygon

        Plotter.draw_power(Self) -> None
        """
        powerlist = []
        for index, power in enumerate(
            self.controller.data.get_power(self.array)):
            entry = self.translator.power_coords(index, power, self.array)
            powerlist.append(entry)
        self.create_polygon(powerlist, fill=POWER_COLOUR,
                            width=1, outline=POWER_COLOUR)
        
    def draw_temp(self):
        """Creates a line that plots the temperature as a line

        plotter.draw_temp(self) -> None
        """
        templist = []
        for index, temp in enumerate(self.controller.data.get_temperature()):
            entry = self.translator.temperature_coords(index, temp)
            templist.append(entry)
        self.create_line(templist, fill='red', width=1)

    def draw_sunlight(self):
        """Creates a line that plots the sunlight as a line

        plotter.draw_sunlight(self) -> None
        """
        sunlist = []
        for index, light in enumerate(self.controller.data.get_sunlight()):
            entry = self.translator.sunlight_coords(index, light)
            sunlist.append(entry)
        self.create_line(sunlist, fill='orange', width=1)

    def index(self, x):
        """Returns the x coordinate for a given index on a plot
        Returns None if goes past window to right

        Plotter.index(int) -> None
        """
        x = self.translator.get_index(x)
        if x > len(self.controller.data.get_temperature())-1 or x <= 0:
            return 
        else:
            self.time = self.controller.data.get_time(x)
            self.temperature = self.controller.data.get_temperature()[x]
            self.sunlight = self.controller.data.get_sunlight()[x]
            self.power = self.controller.data.get_power(self.array)[x]
        

    def draw_line(self, x, y):
        """Creates a vertical black line

        plotter.draw_line(event, int, int) -> None
        """
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

        OptionsFrame.__init__(TkClass, Class) -> None
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
        self.apply = Button(self.entryFrame, text="Apply",
                             command=self.change_date_call)
        self.apply.pack(side=LEFT, padx=5, pady = 10)

        arrays = ARRAYS[-1]
        self.Position = StringVar()
        self.Position.set(arrays)

        self.alist = OptionMenu(
            self, self.Position, *ARRAYS, command=self.change_building_call)
        self.alist.pack(side=RIGHT, anchor = E, fill=X, pady = 10, padx=5)     
        #self.Position holds the array name
        
    def change_building_call(self, event):
        """Tells the controller to change building

        OptionsFrame.change_building_call(event) -> None
        """
        new_array = self.Position.get()
        self.controller.change_array(new_array)

    def check_update(self):
        """Checks the state of update buttons, updates plot accordingly

        OptionsFrame.check_update(None) -> None
        """
        self.controller.update_plot()        

    def change_date_call(self):
        """Calls method to change date

        OptionsFrame.change_date_call(None) -> None
        """
        entry = self.entry.get()
        try:
            self.content = entry
            self.controller.change_date(self.content)
        except ValueError as error:
            tkMessageBox.showerror("Date Error", error.message)

class LabelFrame(Frame):
    """This class is the Frame at the top which holds the label for
    displaying time, tem, date, sunlight etc.

    LabelFrame.__init__(TkClass, Class) -> None
    """
    def __init__(self, master, controller):
        """Creates the label at top of window
        master - top level window
        controller - the app object

        Constructor:LabelFrame(master, parent)
        """
        self.controller = controller
        Frame.__init__(self, master)
        self.printed = None
        self.prettyPrint = Label(self, text=self.printed, anchor=W)
        self.prettyPrint.pack(side=LEFT, pady=5)


class PVPlotApp(object):
    """
    This is the top level class for the GUI. It is responsible for
    creating and
    managing instances of the other classes. 
    """
    def __init__(self, master):
        """Creates a class that holds instances of other classes
        master = top level window

        PVPlotApp.__init__(TkClass) -> None
        """
        master.title("PV Plotter")
        self.master = master
        self.LabelWidget = LabelFrame(master, self)
        self.LabelWidget.pack(fill=X, side=TOP, padx=10, pady=10, anchor=W)
        self.data = PVData()
        self.data.change_date(yesterday())
        self.canvas = Plotter(master, self)
        self.canvas.pack(fill=BOTH, expand=True, padx=10)
        self.widget = OptionsFrame(master, self)
        self.widget.pack(fill=BOTH, anchor=E)
        self.update_plot()
        self.canvas.bind("<Button-1>", self.ButtonPress)
        self.canvas.bind("<Motion>", self.ButtonMotion)
        self.canvas.bind("<ButtonRelease-1>", self.ButtonRelease)
        self.clicked = False
        self.yesterday = self.data.get_date()
        self.widget.entry.insert(0, self.yesterday)
        master.minsize(800, 600)
        
    def ButtonPress(self, event):
        """Event handler for when the Left mouse button has been clicked

        PVPlotApp.ButtonPress(event) -> None
        """
        self.clicked = True
        self.update_plot()
        self.newx = event.x
        self.newy = event.y
        self.canvas.draw_line(self.newx, self.newy)
        self.canvas.index(self.newx)
        self.create_ppdata()
        self.update_label()

        
    def ButtonMotion(self, event):
        """Draws the line in the new position

        PVPlotApp.ButtonMotion(event) -> None
        """
        if self.clicked == True: 
            self.update_plot()
            self.newx = event.x
            self.newy = event.y
            self.canvas.draw_line(self.newx, self.newy)
            self.canvas.index(self.newx)#for the black line
            self.create_ppdata()
            self.update_label()
        else:
            return      

    def ButtonRelease(self, e):
        """Event handler for when the left mouse has been released

        PVPlotApp.ButtonRelease(event) -> None
        """
        self.canvas.delete(ALL)
        self.update_plot()
        self.clicked = False

    def update_plot(self):
        """A method used to update plot according to GUI state

        PVPlotApp.update_plot(None) -> None
        """
        self.canvas.delete(ALL)
        if self.widget.pvar.get() == True:
            self.canvas.draw_power()
        if self.widget.tvar.get() == True:
            self.canvas.draw_temp()
        if self.widget.svar.get() == True:
            self.canvas.draw_sunlight()
        self.LabelWidget.prettyPrint.config(
            text='Data for {0}'.format(self.data.get_date()))

    def change_date(self, dateStr):
        """Changes the date for data and updates plot for new date

        PVPlotApp.change_date(string) -> None
        """
        self.data.change_date(dateStr)
        self.update_plot()
    
    def change_array(self, array):
        """Changes the array for power and updates new power

        PVPlotApp.change_array(string) -> None
        """
        self.canvas.delete(ALL)
        self.canvas.array = array
        self.update_plot()

    def create_ppdata(self):
        """Creates data to be displayed in Pretty Print

        PVPlotApp.create_ppdata(None) -> None
        """     
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
        self.pp = pretty_print_data(
            date, time, temp, sun, power, is_cumulative=False)

    def update_label(self):
        """Updates Label with new Data

        PVPlotApp.update_label(None) -> None
        """
        self.LabelWidget.prettyPrint.config(
            text = self.pp)

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

