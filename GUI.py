from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from TWNBA_sweepplotter import Data, lineplot, set_grid
from tkinter import *  # NOQA
from tkinter import ttk
from tkinter import filedialog

root = Tk()

# Parameters
first_digit_4 = [0, 0, 1, 1]
second_digit_4 = [0, 1, 0, 1]
first_digit_9 = [0, 0, 0, 1, 1, 1, 2, 2, 2]
second_digit_9 = [0, 1, 2, 0, 1, 2, 0, 1, 2]

# Button to load in a file
button_open = Button(root, text="\U0001F4C2", command=lambda: open_files())
button_open.grid(row=0, column=0)


def open_files():
    try:
        canvas.get_tk_widget().grid_forget()
    except:
        pass

    for count in range(9):
        try:
            list_of_lines[count].combo_hue.grid_forget()
            list_of_lines[count].combo_first_param.grid_forget()
            list_of_lines[count].combo_sec_param.grid_forget()
            list_of_lines[count].combo_first_value.grid_forget()
            list_of_lines[count].combo_sec_value.grid_forget()
        except:
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
num_plots_values = ['1', "4", "9"]
combo_num_plots = ttk.Combobox(root, values=num_plots_values, state='disabled')
combo_num_plots.set("How many plots?")
combo_num_plots.grid(row=0, column=1)
button_set_num_plots = Button(root, text='Set', state='disabled',
                              command=lambda: set_num_plots(combo_num_plots.get(), class_data))
button_set_num_plots.grid(row=0, column=2)


def set_num_plots(num, data):
    global num_plots
    global list_of_lines

    try:
        canvas.get_tk_widget().grid_forget()
    except:
        pass

    for count in range(9):
        try:
            list_of_lines[count].combo_hue.grid_forget()
            list_of_lines[count].combo_first_param.grid_forget()
            list_of_lines[count].combo_sec_param.grid_forget()
            list_of_lines[count].combo_first_value.grid_forget()
            list_of_lines[count].combo_sec_value.grid_forget()
        except:
            pass

    num_plots = int(num)
    list_of_lines = []
    lines = 1
    for count in range(num_plots):
        list_of_lines.append(Command(lines, 1, data))
        lines += 1

    button_exec_plot = Button(root, text='Execute', command=lambda: exec_plot())
    button_exec_plot.grid(row=10, column=2, padx=2, pady=2)


# Recipe input
class Command:
    def __init__(self, row, column, data):
        self.combo_first_value = None
        self.combo_sec_value = None
        param_with_none = data.parameters.copy()
        param_with_none.append('None')

        def first_param_update(event):
            self.combo_first_value.config(values=data.dict_of_unique_param[self.combo_first_param.get()])

        def sec_param_update(event):
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
        self.combo_hue.grid(row=row, column=column + 5, padx=2, pady=2)


# Executing the plot
def exec_plot():
    global canvas

    try:
        canvas.get_tk_widget().grid_forget()
    except:
        pass

    set_grid(num_plots)
    for count in range(num_plots):
        try:
            if num_plots == 4:
                plot = lineplot(class_data, first_digit_4[count], second_digit_4[count],
                                list_of_lines[count].combo_hue.get(),
                                list_of_lines[count].combo_first_param.get(),
                                list_of_lines[count].combo_first_value.get(), list_of_lines[count].combo_sec_param.get(),
                                list_of_lines[count].combo_sec_value.get())
            elif num_plots == 9:
                plot = lineplot(class_data, first_digit_9[count], second_digit_9[count],
                                list_of_lines[count].combo_hue.get(),
                                list_of_lines[count].combo_first_param.get(),
                                list_of_lines[count].combo_first_value.get(), list_of_lines[count].combo_sec_param.get(),
                                list_of_lines[count].combo_sec_value.get())
            else:
                plot = 0
        except:
            pass

    if num_plots == 1:
        plot = lineplot(class_data, 'None', 'None',
                        list_of_lines[0].combo_hue.get(),
                        list_of_lines[0].combo_first_param.get(),
                        list_of_lines[0].combo_first_value.get(),
                        list_of_lines[0].combo_sec_param.get(),
                        list_of_lines[0].combo_sec_value.get())

    canvas = FigureCanvasTkAgg(plot, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=12, column=0, columnspan=10, rowspan=10)


root.mainloop()
