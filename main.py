# -*- coding: utf-8 -*-
"""
Created on Thu May  5 22:14:10 2022

@author: wahyu
"""

# Modules
from PyQt5 import QtWidgets, QtCore
import sqlite3
from sys import exit, argv

# Class - Main Window
class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        
        # Setup Main Window
        self.setWindowTitle("Simple Database")
        self.setFixedSize(600, 800)
        
        # Main Window Frame & Layout
        self.mainFrame = QtWidgets.QFrame()
        self.mainLayout = QtWidgets.QVBoxLayout()

        # Create Window Layout - Buttons and Table
        self.createButtons()
        self.createTable()
        
        # Fill Table when app is starting
        self.fillTable()
        
        # Setup Main Frame to Main Window
        self.mainFrame.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainFrame)
        
    # Method - Create Window Layout
    def createButtons(self):
        # Layout is consisted of buttons and table
        
        # Buttons are grouped horizontaly
        group = QtWidgets.QWidget()
        group_ly = QtWidgets.QHBoxLayout()
        group_ly.setContentsMargins(0, 0, 0, 0)
        
        add_button = QtWidgets.QPushButton("Add Data")
        add_button.clicked.connect(self.addDataDialog)
        group_ly.addWidget(add_button)
        
        del_button = QtWidgets.QPushButton("Delete Data")
        del_button.clicked.connect(self.deleteData)
        group_ly.addWidget(del_button)
        
        # Setup buttons group & add to main layout
        group.setLayout(group_ly)
        self.mainLayout.addWidget(group)

    # Method - Create Table
    def createTable(self):
        # Create Table Widget - Setup Number of Row, Columns, Headers
        self.table = QtWidgets.QTableWidget()
        
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["", "Name", "Phone", "Address"])
                
        # Add Table to Main Layout
        self.mainLayout.addWidget(self.table)
        
    # Method Fill - Table
    def fillTable(self):
        # First Get Data from Database then Insert to Table Widget
        
        # Get Data from SQLite Table
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        data = cursor.execute("""SELECT * FROM profile""").fetchall()
        conn.close()
        
        # Adjust row number to data number
        self.table.setRowCount(len(data))
        
        # Fill Table Cells using data from Database
        for i in range(len(data)):
            # Add Check Box
            self.table.setCellWidget(i, 0, QtWidgets.QCheckBox())
            
            for j in range(3):
                self.table.setItem(i, j+1, 
                                   QtWidgets.QTableWidgetItem(str(data[i][j])))
                
        # Setup colum width to fit contents
        self.table.resizeColumnsToContents()
        
    # Method - Add Data
    def addDataDialog(self):
        self.addDialog = QtWidgets.QDialog()
        self.addDialog.setWindowTitle("Add Data")
        dialog_ly = QtWidgets.QGridLayout()
        
        dialog_ly.addWidget(QtWidgets.QLabel("Name"), 0, 0)
        self.name_form = QtWidgets.QLineEdit()
        dialog_ly.addWidget(self.name_form, 0, 1)
        
        dialog_ly.addWidget(QtWidgets.QLabel("Phone"), 1, 0)
        self.phone_form = QtWidgets.QSpinBox()
        self.phone_form.setMinimum(0)
        self.phone_form.setMaximum(999999999)
        dialog_ly.addWidget(self.phone_form, 1, 1)
        
        dialog_ly.addWidget(QtWidgets.QLabel("Address"), 2, 0)
        self.address_form = QtWidgets.QLineEdit()
        dialog_ly.addWidget(self.address_form, 2, 1)
        
        # Add Button
        addButton = QtWidgets.QPushButton("Add Data")
        addButton.clicked.connect(self.addData)
        dialog_ly.addWidget(addButton, 3, 1)
        
        # Setup Dialog
        self.addDialog.setLayout(dialog_ly)
        self.addDialog.exec_()
        
    # Method - Add Data
    def addData(self):
        # Get Data to Tuple for SQLite Insert
        batch = (self.name_form.text(), self.phone_form.value(),
                 self.address_form.text())
        
        # Insert Data to SQL
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        cursor.execute("""INSERT INTO profile VALUES (?, ?, ?)""",
                       batch)
        conn.commit()
        conn.close()
        
        # Update Table 
        self.fillTable()
        
        # Close Forms Dialog
        self.addDialog.close()
        
    # Method - Delete Data
    def deleteData(self):
        # Delete data based on check box
        
        # Connection and Cursor to delete SQL data and fill table
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        # First get name of checked (want to delete)
        # name will be used to delete record on database
        deletedName = []
        for i in range(self.table.rowCount()):
            # Add Name to deleted if checked
            if self.table.cellWidget(i, 0).isChecked():
                deletedName.append(self.table.item(i, 1).text())
                
        # Delete Data From SQL
        for name in deletedName:
            cursor.execute("""DELETE FROM profile WHERE name='{}'""".format(
                name))
        
        # Commit Change
        conn.commit()
        conn.close()
        
        # Refresh table contents
        self.fillTable()
            
# Class - Application
class Main():
    def __init__(self):
        app = QtWidgets.QApplication(argv)
        app.setStyle('Fusion')
        window = mainWindow()
        
        window.show()
        exit(app.exec_())

# Run Application
if __name__ == "__main__":
    Main()
