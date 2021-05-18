from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from TWNBA_sweepplotter import Data, lineplot, set_grid, save_plot, kdeplot
from tkinter import *  # NOQA
from tkinter import ttk
from tkinter import filedialog
from itertools import cycle

root = Tk()
root.title('TWNBA Sweepplotter')
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w * 0.5, h * 0.5))


# Parameters
global canvas
global class_data
global num_plots, sec_cycle_value, sec_cycle, first_cycle
global list_of_lines
first_digit_4 = [0, 0, 1, 1]
second_digit_4 = [0, 1, 0, 1]
first_digit_9 = [0, 0, 0, 1, 1, 1, 2, 2, 2]
second_digit_9 = [0, 1, 2, 0, 1, 2, 0, 1, 2]
first_digit_16 = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
second_digit_16 = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]

# Button to load in a file
button_open = Button(root, text="open", command=lambda: open_files())
button_open.grid(row=0, column=0)


def open_files():
    try:
        canvas.get_tk_widget().destroy()
    except NameError:
        pass

    for count in range(9):
        try:
            list_of_lines[count].combo_hue.grid_forget()
            list_of_lines[count].combo_first_param.grid_forget()
            list_of_lines[count].combo_sec_param.grid_forget()
            list_of_lines[count].combo_first_value.grid_forget()
            list_of_lines[count].combo_sec_value.grid_forget()
        except (NameError, IndexError):
            pass

    file_name = filedialog.askopenfilename(title="Open File",
                                           filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
                                           )
    global class_data
    class_data = Data(file_name)

    text.delete('1.0', END)
    text.insert("end", "File name: " + file_name.split('/')[-1]
                + "\n" "parameters: " + str(class_data.parameters)
                + "\n" "sweep: " + str(class_data.sweep) + "\n" "steps: "
                + str(class_data.steps) + "\n" "runs: "
                + str(class_data.runs) + "\n")
    text.see("end")
    combo_num_plots.config(state='readonly')
    button_set_num_plots.config(state='normal')


# Placement of the log
text = Text(root, width=40, height=8)
text.grid(row=0, column=3, columnspan=10)

# Combo to pick the number of plots
num_plots_values = ['1', "4", "9", "16"]
combo_num_plots = ttk.Combobox(root, values=num_plots_values, state='disabled')
combo_num_plots.set("How many plots?")
combo_num_plots.grid(row=0, column=1)
button_set_num_plots = Button(root, text='Set', state='disabled',
                              command=lambda: set_num_plots(combo_num_plots.get(), class_data))
button_set_num_plots.grid(row=0, column=2)


def set_num_plots(num, data):
    global num_plots, sec_cycle_value, sec_cycle, first_cycle
    global list_of_lines

    try:
        canvas.get_tk_widget().destroy()
    except NameError:
        pass

    for count in range(16):
        try:
            list_of_lines[count].combo_hue.grid_forget()
            list_of_lines[count].combo_first_param.grid_forget()
            list_of_lines[count].combo_sec_param.grid_forget()
            list_of_lines[count].combo_first_value.grid_forget()
            list_of_lines[count].combo_sec_value.grid_forget()
        except (NameError, IndexError):
            pass

    num_plots = int(num)
    list_of_lines = []
    lines = 1
    for count in range(num_plots):
        list_of_lines.append(Command(lines, 1, data))
        lines += 1

    try:
        first_cycle = cycle(range(len(data.dict_of_unique_param[list_of_lines[0].combo_first_param.get()])))
    except KeyError:
        pass

    try:
        sec_cycle = cycle(range(len(data.dict_of_unique_param[list_of_lines[0].combo_sec_param.get()])))
    except KeyError:
        pass
    cycle_help = [1, 0, 0, 1, 0, 0, 1, 0, 0]
    cycle_help_16 = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
    cycle_count = 0

    if num_plots == 4:
        for line in list_of_lines:
            first_cycle_value = next(first_cycle)
            line.combo_first_value.current(first_cycle_value)

    if num_plots == 9:
        for line in list_of_lines:
            first_cycle_value = next(first_cycle)
            line.combo_first_value.current(first_cycle_value)
            try:
                if cycle_help[cycle_count] == 1:
                    sec_cycle_value = next(sec_cycle)
                line.combo_sec_value.current(sec_cycle_value)
            except (TclError, NameError):
                pass
            cycle_count += 1

    if num_plots == 16:
        for line in list_of_lines:
            first_cycle_value = next(first_cycle)
            line.combo_first_value.current(first_cycle_value)
            try:
                if cycle_help_16[cycle_count] == 1:
                    sec_cycle_value = next(sec_cycle)
                line.combo_sec_value.current(sec_cycle_value)
            except (TclError, NameError):
                pass
            cycle_count += 1

    button_exec_lineplot = Button(root, text='Execute Lineplot', command=lambda: exec_plot('line'))
    button_exec_lineplot.grid(row=34, column=3)

    button_exec_kdeplot = Button(root, text='Execute Kdeplot', command=lambda: exec_plot('kde'))
    button_exec_kdeplot.grid(row=34, column=4)


# Recipe input
class Command:
    def __init__(self, row, column, data):
        self.combo_first_value = None
        self.combo_sec_value = None
        param_with_none = data.parameters.copy()
        param_with_none.append('None')

        def first_param_update(_):
            self.combo_first_value.config(values=data.dict_of_unique_param[self.combo_first_param.get()])

        def sec_param_update(_):
            if self.combo_sec_param.get() == 'None':
                self.combo_sec_value.config(values=['None'])
                self.combo_sec_value.current(0)
            else:
                self.combo_sec_value.config(values=data.dict_of_unique_param[self.combo_sec_param.get()])

        self.combo_first_param = ttk.Combobox(root, values=data.parameters, state='readonly')
        self.combo_first_param.set("First parameter")
        self.combo_first_param.grid(row=row, column=column, padx=2, pady=2)
        self.combo_first_param.bind("<<ComboboxSelected>>", first_param_update)

        self.combo_first_value = ttk.Combobox(root, state='readonly', values=['None'])
        self.combo_first_value.set("First value")
        self.combo_first_value.grid(row=row, column=column + 1, padx=2, pady=2)

        self.combo_sec_param = ttk.Combobox(root, values=param_with_none, state='readonly')
        self.combo_sec_param.set("Second parameter")
        self.combo_sec_param.grid(row=row, column=column + 2, padx=2, pady=2)
        self.combo_sec_param.bind("<<ComboboxSelected>>", sec_param_update)

        self.combo_sec_value = ttk.Combobox(root, state='readonly', values=['None'])
        self.combo_sec_value.set("Second value")
        self.combo_sec_value.grid(row=row, column=column + 3, padx=2, pady=2)

        self.combo_hue = ttk.Combobox(root, values=data.parameters, state='readonly')
        self.combo_hue.set("hue")
        self.combo_hue.grid(row=row, column=column + 4, padx=2, pady=2)

        # Set the inital selected parameters
        if num_plots == 4:
            self.combo_first_param.current(1)
            self.combo_sec_param.current(2)
            self.combo_hue.current(0)
            first_param_update('_')
            sec_param_update('_')

        if num_plots == 9:
            self.combo_first_param.current(1)
            self.combo_sec_param.current(2)
            self.combo_hue.current(0)
            first_param_update('_')
            sec_param_update('_')

        if num_plots == 16:
            self.combo_first_param.current(1)
            self.combo_sec_param.current(2)
            self.combo_hue.current(0)
            first_param_update('_')
            sec_param_update('_')


# Executing the plot
def exec_plot(kind):
    global canvas
    plot = None

    try:
        canvas.get_tk_widget().destroy()
    except NameError:
        pass

    set_grid(num_plots)

    if kind == 'line':
        for count in range(num_plots):
            try:
                if num_plots == 4:
                    plot = lineplot(class_data, first_digit_4[count], second_digit_4[count],
                                    list_of_lines[count].combo_hue.get(),
                                    list_of_lines[count].combo_first_param.get(),
                                    list_of_lines[count].combo_first_value.get(),
                                    list_of_lines[count].combo_sec_param.get(),
                                    list_of_lines[count].combo_sec_value.get())
                elif num_plots == 9:
                    plot = lineplot(class_data, first_digit_9[count], second_digit_9[count],
                                    list_of_lines[count].combo_hue.get(),
                                    list_of_lines[count].combo_first_param.get(),
                                    list_of_lines[count].combo_first_value.get(),
                                    list_of_lines[count].combo_sec_param.get(),
                                    list_of_lines[count].combo_sec_value.get())

                elif num_plots == 16:
                    plot = lineplot(class_data, first_digit_16[count], second_digit_16[count],
                                    list_of_lines[count].combo_hue.get(),
                                    list_of_lines[count].combo_first_param.get(),
                                    list_of_lines[count].combo_first_value.get(),
                                    list_of_lines[count].combo_sec_param.get(),
                                    list_of_lines[count].combo_sec_value.get())

                else:
                    plot = 0
            except (TypeError, KeyError):
                pass

        if num_plots == 1:
            plot = lineplot(class_data, 'None', 'None',
                            list_of_lines[0].combo_hue.get(),
                            list_of_lines[0].combo_first_param.get(),
                            list_of_lines[0].combo_first_value.get(),
                            list_of_lines[0].combo_sec_param.get(),
                            list_of_lines[0].combo_sec_value.get())

    if kind == 'kde':
        for count in range(num_plots):
            try:
                if num_plots == 4:
                    plot = kdeplot(class_data, first_digit_4[count], second_digit_4[count],
                                   list_of_lines[count].combo_hue.get(),
                                   list_of_lines[count].combo_first_param.get(),
                                   list_of_lines[count].combo_first_value.get(),
                                   list_of_lines[count].combo_sec_param.get(),
                                   list_of_lines[count].combo_sec_value.get())
                elif num_plots == 9:
                    plot = kdeplot(class_data, first_digit_9[count], second_digit_9[count],
                                   list_of_lines[count].combo_hue.get(),
                                   list_of_lines[count].combo_first_param.get(),
                                   list_of_lines[count].combo_first_value.get(),
                                   list_of_lines[count].combo_sec_param.get(),
                                   list_of_lines[count].combo_sec_value.get())

                elif num_plots == 16:
                    plot = lineplot(class_data, first_digit_16[count], second_digit_16[count],
                                    list_of_lines[count].combo_hue.get(),
                                    list_of_lines[count].combo_first_param.get(),
                                    list_of_lines[count].combo_first_value.get(),
                                    list_of_lines[count].combo_sec_param.get(),
                                    list_of_lines[count].combo_sec_value.get())

                else:
                    plot = 0
            except (TypeError, KeyError):
                pass

        if num_plots == 1:
            plot = kdeplot(class_data, 'None', 'None',
                           list_of_lines[0].combo_hue.get(),
                           list_of_lines[0].combo_first_param.get(),
                           list_of_lines[0].combo_first_value.get(),
                           list_of_lines[0].combo_sec_param.get(),
                           list_of_lines[0].combo_sec_value.get())

    root2 = Toplevel()

    canvas = FigureCanvasTkAgg(plot, master=root2)
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1.0)
    canvas.draw()

    # Saving function
    button_save = Button(root, text="save", command=lambda: save_files())
    button_save.grid(row=34, column=5)


def save_files():
    file_name = filedialog.asksaveasfilename(title="Save File",
                                             filetypes=(("PNG Files", "*.png"), ("All Files", "*.*"))
                                             )
    save_plot(file_name, num_plots)


root.mainloop()
