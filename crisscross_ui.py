import math
import numpy as np
import tkFileDialog
import tkMessageBox
import crisscross as crs
import platform
from copy import copy
from sympy import *
from Tkinter import *

WINDOW_SIZE = 360000
MAX_SIZE_OF_BOARD = 15
DEFAULT_WIDTH = 10
DEFAULT_HEIGHT = 4

class CrissCrossUI:
    def __init__(self, master):
        self.master = master

        self.master.title("Criss-cross method for feasibility")
        self.master.geometry("320x200")

        self.variable_string_var = StringVar()
        self.constraint_string_var = StringVar()

        self.nr_of_variables = DEFAULT_WIDTH
        self.nr_of_constraints = DEFAULT_HEIGHT

        self.title_label = Label(self.master, text="Criss-cross method for feasibility")
        self.title_label.pack()

        self.variable_label = Label(self.master, text="Number of variables")
        self.variable_label.pack()
        self.variable_entry = Entry(self.master, textvariable=self.variable_string_var)
        self.variable_entry.pack()

        self.constraint_label = Label(self.master, text="Number of constraints")
        self.constraint_label.pack()
        self.constraint_entry = Entry(self.master, textvariable=self.constraint_string_var)
        self.constraint_entry.pack()

        self.open_file = Button(self.master, text='Import from file', command=self.open_file)
        self.open_file.pack()

        self.start_button = Button(self.master, text="Start", command=self.start_entry_for_vars_and_constrs)
        self.start_button.pack()

        self.close_button = Button(self.master, text="Close", command=self.master.quit)
        self.close_button.pack()

        self.linux_size_w=50
        self.linux_size_h=30

        self.windows_size_w=45
        self.windows_size_h=30

        self.file_matrix = []
        self.matrix = []

    def open_file(self):
        f = tkFileDialog.askopenfile(mode='r')
        lines = f.readlines()
        f.close()
        for line in lines:
            line = line.split(",")
            line[-1] = line[-1].replace("\n", "")
            line[-1] = line[-1].replace("\r", "")
            self.file_matrix.append(line)

        self.variable_entry.insert(0, len(self.file_matrix[0])-2)
        self.constraint_entry.insert(0, len(self.file_matrix))

    def start_entry_for_vars_and_constrs(self):
        if self.is_valid():
            print "Starting ..."
            self.clear_frame()
            if platform.system() == "Linux":
                self.master.geometry(str((self.nr_of_variables + 4) * self.linux_size_w) + "x" + str((self.nr_of_constraints + 2) * self.linux_size_h))
            elif platform.system() == "Windows":
                self.master.geometry(str((self.nr_of_variables + 4) * self.windows_size_w) + "x" + str((self.nr_of_constraints + 2) * self.windows_size_h))
            self.create_entry_for_vars_and_constrs()
        else:
            tkMessageBox.showinfo("Error", "Too many variables and/or constraints!")

    def create_entry_for_vars_and_constrs(self):
        print "Creating the entry..."
        self.button_width = 40
        self.button_height = 20

        label_A = Label(self.master, text="A")
        label_A.grid(row=0, column=int(round(self.nr_of_variables/2)))

        label_eq = Label(self.master, text="<=/>=/=")
        label_eq.grid(row=0, column=self.nr_of_variables)

        label_b = Label(self.master, text="b")
        label_b.grid(row=0, column=self.nr_of_variables+1)

        for i in xrange(self.nr_of_constraints):
            tmp = []
            for j in xrange(self.nr_of_variables+2):
                frame = Frame(self.master, width=self.button_width, height=self.button_height)
                frame.rowconfigure(0, weight=1)
                frame.columnconfigure(0, weight=1)
                frame.grid_propagate(0)
                coefficient = Entry(frame, textvariable=StringVar())
                tmp.append(coefficient)
                frame.grid(row=i+1, column=j, padx=5, pady=5)
                coefficient.grid(sticky="NWSE")
            self.matrix.append(tmp)

        check_feasibility = Button(self.master, text="Check Feasibility", command=self.check_feasibility)
        check_feasibility.grid(row=self.nr_of_constraints+2, column=self.nr_of_variables)     

        if self.file_matrix != []:
            for i in xrange(self.nr_of_constraints):
                for j in xrange(self.nr_of_variables+2):
                    self.matrix[i][j].insert(0, self.file_matrix[i][j])

    def check_feasibility(self):
        pivots = crs.criss_cross(self.nr_of_constraints, self.nr_of_variables, self.parse_coeffs_and_constraints())
        self.clear_frame()

        self.linux_size_w2 = 73
        self.linux_size_h2 = 30

        self.windows_size_w2 = 68
        self.windows_size_h2 = 30

        if platform.system() == "Linux":
            self.master.geometry(str((self.nr_of_variables + 4) * self.linux_size_w2) + "x" + str((self.nr_of_constraints + 2) * self.linux_size_h2 + 30))
        elif platform.system() == "Windows":
            self.master.geometry(str((self.nr_of_variables + 4) * self.windows_size_w2) + "x" + str((self.nr_of_constraints + 2) * self.windows_size_h2 + 30))

        
        self.display_pivot_steps(pivots)

    def display_pivot_steps(self, pivots):
        if pivots[0] == 0:
            Label(self.master, text="Feasible basis found.", font=("Helvetica", 12)).pack()
        else:
            Label(self.master, text="Primal infeasible linear problem.", font=("Helvetica", 12)).pack()

        self.feasibile = (pivots[0]==0)    
        self.pivot_positions = pivots[1]
        self.pivot_tables = pivots[2]
        self.basic_solution_indices = pivots[3]
        self.number_of_steps = len(pivots[2])
        
        self.linux_size_frame_w = 63
        self.linux_size_frame_h = 30

        self.windows_size_frame_w = 58
        self.windows_size_frame_h = 30

        if platform.system() == "Linux":
            frame = Frame(self.master, width=self.linux_size_frame_w*self.pivot_tables[0].shape[1], height=self.linux_size_frame_h*self.pivot_tables[0].shape[0], bg="white")
        elif platform.system() == "Windows":
            frame = Frame(self.master, width=self.windows_size_frame_w*self.pivot_tables[0].shape[1], height=self.windows_size_frame_h*self.pivot_tables[0].shape[0], bg="white")
        
        frame.grid_propagate(0)

        self.pivot_tables_labels = []
        for i in xrange(self.pivot_tables[0].shape[0]):
            tmp = []
            for j in xrange(self.pivot_tables[0].shape[1]):
                if j == (self.pivot_tables[0].shape[1]-1):
                    item = Label(frame, text=str(float(format(float(self.pivot_tables[0][i, j]), '.2f'))), width=6, bg="silver")
                else:
                    item = Label(frame, text=str(float(format(float(self.pivot_tables[0][i, j]), '.2f'))), width=6, bg="white")
                tmp.append(item)
                item.grid(row=i+1, column=j, padx=5, pady=5)
            self.pivot_tables_labels.append(tmp)

        frame.pack()

        if (self.number_of_steps > 1):
            self.pivot_tables_labels[self.pivot_positions[0][0]][self.pivot_positions[0][1]].configure(bg="green")

        self.current_step = 0
        self.previous_button = Button(self.master, text="Previous", width=10, command=lambda step=-1: self.show_step(step), state=DISABLED)
        self.previous_button.pack(side=LEFT, padx=15)
        self.next_button = Button(self.master, text="Next", width=10, command=lambda step=1: self.show_step(step))
        self.next_button.pack(side=RIGHT, padx=15)

        if (self.number_of_steps == 1):
            self.set_button_state(1, DISABLED)
            if (self.feasibile):
                self.show_basic_solutions()

    def set_button_state(self, button, state):
        if button == -1:
            self.previous_button.config(state=state)
        else:
            self.next_button.config(state=state)

    def show_basic_solutions(self):
        solutions = []
        solution = ''

        for i in xrange(0,len(self.basic_solution_indices[self.current_step])):
            if(self.basic_solution_indices[self.current_step][i] < self.nr_of_variables):
                solutions.append("  " + "x" + str(self.basic_solution_indices[self.current_step][i]+1) + "=" + str(format(float(self.pivot_tables[self.current_step].col(-1)[i]), '.2f')) + "\n")
            else:
                solutions.append("  " + "s" + str(self.basic_solution_indices[self.current_step][i]-self.nr_of_variables + 1) + "=" + str(format(float(self.pivot_tables[self.current_step].col(-1)[i]), '.2f')) + "\n")
        
        solution = ''.join([s for (i,s) in sorted(zip(self.basic_solution_indices[self.current_step],solutions))])
        tkMessageBox.showinfo("", ''.join(["Feasible basic solution:\n", solution]))

    def show_step(self, step):
        self.current_step += step
        if ((self.current_step > 0) and (self.current_step < self.number_of_steps)) or ((self.current_step == 0) and (step == -1)):
            self.set_button_state(-step, NORMAL)
        for i in xrange(self.pivot_tables[self.current_step].shape[0]):
            for j in xrange(self.pivot_tables[self.current_step].shape[1]):
                self.pivot_tables_labels[i][j].config(text=str(float(format(float(self.pivot_tables[self.current_step][i, j]), '.2f'))))

        if not ((self.current_step+1 == len(self.pivot_positions)) and (step == -1)):
            self.pivot_tables_labels[self.pivot_positions[self.current_step-step][0]][self.pivot_positions[self.current_step-step][1]].configure(bg="white")
        if self.current_step < self.number_of_steps-1:
            self.pivot_tables_labels[self.pivot_positions[self.current_step][0]][self.pivot_positions[self.current_step][1]].configure(bg="green") 

        if (self.current_step+1 == self.number_of_steps) or (self.current_step == 0):
            self.set_button_state(step, DISABLED)
            if (step == 1 & self.feasibile):
                self.show_basic_solutions()

    def parse_coeffs_and_constraints(self):
        transform = {"<=":1, "=":0, ">=":-1}

        A = np.reshape([float(self.matrix[i][j].get()) for i in xrange(0,self.nr_of_constraints) for j in xrange(0, self.nr_of_variables)], (self.nr_of_constraints, self.nr_of_variables))
        eq = np.diag([transform[self.matrix[i][self.nr_of_variables].get()] for i in xrange(0, self.nr_of_constraints)])
        slacks = np.transpose(eq[~np.all(eq == 0, axis=1)])
        b = np.reshape([float(self.matrix[i][self.nr_of_variables+1].get()) for i in xrange(0, self.nr_of_constraints)], (self.nr_of_constraints, 1))

        A_b = np.concatenate((A, slacks, b), axis=1)

        print A_b

        return(Matrix(A_b))
    
    def clear_frame(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def is_valid(self):
        try:
            self.nr_of_variables = int(self.variable_string_var.get())
            self.nr_of_constraints = int(self.constraint_string_var.get())
        except ValueError:
            return False
        if self.nr_of_variables in xrange(0, MAX_SIZE_OF_BOARD) and self.nr_of_constraints in xrange(0, MAX_SIZE_OF_BOARD):
            return True
        return False

class CrissCross:

    def main(self):
        root = Tk()
        criss_cross_ui = CrissCrossUI(root)
        root.mainloop()

if __name__ == '__main__':
    criss_cross = CrissCross()
    criss_cross.main()