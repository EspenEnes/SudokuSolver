import sys
from collections import namedtuple
from itertools import product

import numpy as np
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QVariant, QModelIndex, QRegExp, pyqtSlot, QRunnable, QThreadPool, pyqtSignal, QObject
from PyQt5.QtGui import QIntValidator, QRegExpValidator, QValidator
from PyQt5.QtWidgets import QApplication, QDataWidgetMapper, QItemDelegate, QTableView
import pandas as pd

from QT_Designes import soduku_window
import json
import time


class NotEmptyValidator(QValidator):
    def validate(self, text, pos):
        if text in ["1", "2", "3", "4", "5", "6", "7", "8", "9", ""]:
            state = QIntValidator.Acceptable
        else:
            state = QIntValidator.Invalid
        return state, text, pos

class manager(QtCore.QAbstractTableModel):
    def __init__(self, data=None):
        super(manager, self).__init__()
        self._data = data  # or pd.DataFrame("", index=range(9), columns=["A", "B", "C", "D", "E", "F", "G", "H", "I"])

    def data(self, index, role):
        row = index.row()
        col = index.column()
        if role == Qt.DisplayRole:
            return str(self._data.iloc[row, col])
        if role == Qt.EditRole:
            return str(self._data.iloc[row, col])
        else:
            QVariant

    def rowCount(self, parent):
        return len(self._data.values)

    def update(self):
        pass

    def columnCount(self, parent):
        return self._data.columns.size

    def setData(self, index, value, role):
        if not index.isValid() or role != Qt.EditRole:
            return False
        row = index.row()
        col = index.column()
        if role == Qt.EditRole:
            self._data.iloc[row, col] = str(value)
            self.dataChanged.emit(index, index)
            return True
        return True

class Soduku(QtWidgets.QMainWindow, soduku_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Soduku, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.toggled.connect(self.enable)
        self.pushButton_2.clicked.connect(self.solve)
        self.initLine()
        self.colums = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        self.progressBar.setMaximum(100)
        self.progressBar.setMinimum(0)
        self.progressBar.setValue(0)
        # self.progressBar.hide()

        data = {}

        for column in self.colums:
            data[column] = [v for k, v in sorted({x.objectName(): x.text() for x in
                                                  self.findChildren(QtWidgets.QLineEdit,
                                                                    QtCore.QRegExp(f"{column}"))}.items())]
        # self.df = pd.DataFrame.from_dict(json.load(open("test.json")))

        self.df = pd.DataFrame.from_dict(data, dtype="int")
        self.model = manager(self.df)

        self.mapperA = QDataWidgetMapper()
        self.mapperA.setModel(self.model)
        self.mapperA.setCurrentIndex(0)
        self.mapperA.addMapping(self.A1, 0)
        self.mapperA.addMapping(self.B1, 1)
        self.mapperA.addMapping(self.C1, 2)
        self.mapperA.addMapping(self.D1, 3)
        self.mapperA.addMapping(self.E1, 4)
        self.mapperA.addMapping(self.F1, 5)
        self.mapperA.addMapping(self.G1, 6)
        self.mapperA.addMapping(self.H1, 7)
        self.mapperA.addMapping(self.I1, 8)

        self.mapperB = QDataWidgetMapper()
        self.mapperB.setModel(self.model)
        self.mapperB.setCurrentIndex(1)
        self.mapperB.addMapping(self.A2, 0)
        self.mapperB.addMapping(self.B2, 1)
        self.mapperB.addMapping(self.C2, 2)
        self.mapperB.addMapping(self.D2, 3)
        self.mapperB.addMapping(self.E2, 4)
        self.mapperB.addMapping(self.F2, 5)
        self.mapperB.addMapping(self.G2, 6)
        self.mapperB.addMapping(self.H2, 7)
        self.mapperB.addMapping(self.I2, 8)

        self.mapperC = QDataWidgetMapper()
        self.mapperC.setModel(self.model)
        self.mapperC.setCurrentIndex(2)
        self.mapperC.addMapping(self.A3, 0)
        self.mapperC.addMapping(self.B3, 1)
        self.mapperC.addMapping(self.C3, 2)
        self.mapperC.addMapping(self.D3, 3)
        self.mapperC.addMapping(self.E3, 4)
        self.mapperC.addMapping(self.F3, 5)
        self.mapperC.addMapping(self.G3, 6)
        self.mapperC.addMapping(self.H3, 7)
        self.mapperC.addMapping(self.I3, 8)

        self.mapperD = QDataWidgetMapper()
        self.mapperD.setModel(self.model)
        self.mapperD.setCurrentIndex(3)
        self.mapperD.addMapping(self.A4, 0)
        self.mapperD.addMapping(self.B4, 1)
        self.mapperD.addMapping(self.C4, 2)
        self.mapperD.addMapping(self.D4, 3)
        self.mapperD.addMapping(self.E4, 4)
        self.mapperD.addMapping(self.F4, 5)
        self.mapperD.addMapping(self.G4, 6)
        self.mapperD.addMapping(self.H4, 7)
        self.mapperD.addMapping(self.I4, 8)

        self.mapperE = QDataWidgetMapper()
        self.mapperE.setModel(self.model)
        self.mapperE.setCurrentIndex(4)
        self.mapperE.addMapping(self.A5, 0)
        self.mapperE.addMapping(self.B5, 1)
        self.mapperE.addMapping(self.C5, 2)
        self.mapperE.addMapping(self.D5, 3)
        self.mapperE.addMapping(self.E5, 4)
        self.mapperE.addMapping(self.F5, 5)
        self.mapperE.addMapping(self.G5, 6)
        self.mapperE.addMapping(self.H5, 7)
        self.mapperE.addMapping(self.I5, 8)

        self.mapperF = QDataWidgetMapper()
        self.mapperF.setModel(self.model)
        self.mapperF.setCurrentIndex(5)
        self.mapperF.addMapping(self.A6, 0)
        self.mapperF.addMapping(self.B6, 1)
        self.mapperF.addMapping(self.C6, 2)
        self.mapperF.addMapping(self.D6, 3)
        self.mapperF.addMapping(self.E6, 4)
        self.mapperF.addMapping(self.F6, 5)
        self.mapperF.addMapping(self.G6, 6)
        self.mapperF.addMapping(self.H6, 7)
        self.mapperF.addMapping(self.I6, 8)

        self.mapperG = QDataWidgetMapper()
        self.mapperG.setModel(self.model)
        self.mapperG.setCurrentIndex(6)
        self.mapperG.addMapping(self.A7, 0)
        self.mapperG.addMapping(self.B7, 1)
        self.mapperG.addMapping(self.C7, 2)
        self.mapperG.addMapping(self.D7, 3)
        self.mapperG.addMapping(self.E7, 4)
        self.mapperG.addMapping(self.F7, 5)
        self.mapperG.addMapping(self.G7, 6)
        self.mapperG.addMapping(self.H7, 7)
        self.mapperG.addMapping(self.I7, 8)

        self.mapperH = QDataWidgetMapper()
        self.mapperH.setModel(self.model)
        self.mapperH.setCurrentIndex(7)
        self.mapperH.addMapping(self.A8, 0)
        self.mapperH.addMapping(self.B8, 1)
        self.mapperH.addMapping(self.C8, 2)
        self.mapperH.addMapping(self.D8, 3)
        self.mapperH.addMapping(self.E8, 4)
        self.mapperH.addMapping(self.F8, 5)
        self.mapperH.addMapping(self.G8, 6)
        self.mapperH.addMapping(self.H8, 7)
        self.mapperH.addMapping(self.I8, 8)

        self.mapperI = QDataWidgetMapper()
        self.mapperI.setModel(self.model)
        self.mapperI.setCurrentIndex(8)
        self.mapperI.addMapping(self.A9, 0)
        self.mapperI.addMapping(self.B9, 1)
        self.mapperI.addMapping(self.C9, 2)
        self.mapperI.addMapping(self.D9, 3)
        self.mapperI.addMapping(self.E9, 4)
        self.mapperI.addMapping(self.F9, 5)
        self.mapperI.addMapping(self.G9, 6)
        self.mapperI.addMapping(self.H9, 7)
        self.mapperI.addMapping(self.I9, 8)
        self.threadpool = QThreadPool()

        index1 = self.model.createIndex(0, 0)
        index2 = self.model.createIndex(8, 8)
        self.model.dataChanged.emit(index1, index2)

        self.view = QtWidgets.QTableView()
        self.view.setModel(self.model)

    def enable(self, checked):
        for child in self.findChildren(QtWidgets.QLineEdit):
            child.setEnabled(checked)

    def initLine(self):
        for child in self.findChildren(QtWidgets.QLineEdit):
            validator = NotEmptyValidator(child)
            child.setValidator(validator)

    def solve(self):
        self.start = time.time()

        # Do a easy solve
        solve = Solve(self.model._data)
        solve.signals.result.connect(self.result)
        solve.signals.finished.connect(self.finished)
        self.threadpool.start(solve)

        # If easy solved gave no solution, try to to guess one number and solve!
    def solve_2(self, dataframe):
        self.progressBar.show()
        solve2 = Solve2(dataframe)
        solve2.signals.result.connect(self.result2)
        solve2.signals.finished.connect(self.finished)
        solve2.signals.progress.connect(self.progress)
        self.threadpool.start(solve2)

    def progress(self, progress):
        self.progressBar.setValue(progress)


    def result(self, dataframe):
        self.model._data = dataframe
        index1 = self.model.createIndex(0, 0)
        index2 = self.model.createIndex(8, 8)
        self.model.dataChanged.emit(index1, index2)

        if "" in dataframe.values:
            # If easy solved gave no solution, try to to guess one number and solve!
            self.solve_2(dataframe)



    def result2(self, dataframe):
        self.model._data = dataframe
        index1 = self.model.createIndex(0, 0)
        index2 = self.model.createIndex(8, 8)
        self.model.dataChanged.emit(index1, index2)

        if "" in dataframe.values:
            self.progressBar.setTextVisible(True)
            self.progressBar.setFormat("Failed to solve current soduku")
            self.progressBar.setAlignment(Qt.AlignCenter)



    def finished(self):
        self.progressBar.setValue(100)
        self.progressBar.setFormat(f"Solved in {(time.time() - self.start):.2f} s ")
        self.progressBar.setAlignment(Qt.AlignCenter)

    def thread_complete(self):
        print("Done")

    def product_dict(self, inp):
        return (dict(zip(inp.keys(), values)) for values in product(*inp.values()))


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(pd.DataFrame)
    progress = pyqtSignal(int)

class Solve(QRunnable):
    def __init__(self, dataframe):
        super(Solve, self).__init__()
        self.solved = False
        self.a = pd.Series(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
        self.df = dataframe.copy()
        self.signals = WorkerSignals()

    def run(self) -> None:
        solved = self.SodukuAlgo(self.df)
        if solved:
            self.signals.finished.emit()
            self.signals.result.emit(self.df)
        else:
            self.signals.result.emit(self.df)

    def getneigbors(self,dataframe,missing, index):
        row = int(index[0])
        col = index[1]
        col_i = dataframe.columns.get_loc(col)
        if int(row) > 0:
            Hor1 = dataframe.iloc[int(row) - 1, :]
        else:
            Hor1 = self.a
        if int(row) < 8:
            Hor2 = dataframe.iloc[int(row) + 1, :]
        else:
            Hor2 = self.a
        if col_i > 0:
            Ver1 = dataframe.iloc[:, col_i - 1]
        else:
            Ver1 = self.a
        if col_i < 8:
            Ver2 = dataframe.iloc[:, col_i + 1]
        else:
            Ver2 = self.a

        if missing[0] in Hor1.values:
            if missing[0] in Hor2.values:
                if missing[0] in Ver1.values:
                    if missing[0] in Ver2.values:
                        return True
        return False


    def SodukuAlgo(self, dataframe, test=False):
        self.run = True
        while self.run:
            self.run = False
            for index in self.getempty(dataframe):
                missing = self.findMissing(dataframe, index)

                #If only missing one number in row or culumn insert number
                if len(missing) == 1:
                    self.run = True
                    self.InsertNumber(dataframe, missing[0], index, test=test)
                    continue
                elif len(missing) == 0:
                    """If we get zero missing during an evaluation the solving has failed during Solve2 where we guess numbers"""
                    self.run = False
                    break

                #if neigboring rows,columns contains number, insert number
                if self.getneigbors(dataframe,missing[0],index):
                    self.run = True
                    self.InsertNumber(dataframe, missing[0], index, test=test)

        return "" not in dataframe.values

    def findMissing(self, dataframe, index):
        row = int(index[0])
        col = index[1]
        horizontal = dataframe.iloc[int(row)]
        vertical = dataframe[col]
        if int(row) < 3:
            if col in ["A", "B", "C"]:
                box = dataframe.iloc[0:3, 0:3].unstack()
            elif col in ["D", "E", "F"]:
                box = dataframe.iloc[0:3, 3:6].unstack()
            elif col in ["G", "H", "I"]:
                box = dataframe.iloc[0:3, 6:9].unstack()

        elif int(row) > 2 and int(row) < 6:
            if col in ["A", "B", "C"]:
                box = dataframe.iloc[3:6, 0:3].unstack()
            elif col in ["D", "E", "F"]:
                box = dataframe.iloc[3:6, 3:6].unstack()
            elif col in ["G", "H", "I"]:
                box = dataframe.iloc[3:6, 6:9].unstack()
        elif int(row) > 5:
            if col in ["A", "B", "C"]:
                box = dataframe.iloc[6:9, 0:3].unstack()
            elif col in ["D", "E", "F"]:
                box = dataframe.iloc[6:9, 3:6].unstack()
            elif col in ["G", "H", "I"]:
                box = dataframe.iloc[6:9, 6:9].unstack()
        return self.a.mask(self.a.isin(pd.concat([horizontal, vertical, box]).values)).dropna().to_list()

    def getempty(self, dataframe):
        result = []
        for col in dataframe.columns:
            for row in dataframe[col].where(dataframe[col].values == "").dropna().index:
                result.append((f"{row}{col}"))
        return result

    def InsertNumber(self, dataframe, number, index, test=False):
        row = int(index[0])
        col = index[1]
        dataframe[col][row] = number[0]

class Solve2(Solve):
    def __init__(self, dataframe):
        super(Solve, self).__init__()
        self.solved = False
        self.a = pd.Series(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
        self.df = dataframe.copy()
        self.df_original = dataframe
        self.signals = WorkerSignals()

    def run(self):
        empty_indexes = self.getempty(self.df)
        b = {}
        for aa in empty_indexes:
            missing = self.findMissing(self.df, aa)
            missing.append("")
            b[aa] = missing
        for enum, index in enumerate(b):
            if self.solved: break
            self.signals.progress.emit(int((enum / len(b)) * 100.0))
            row = index[0]
            col = index[1]
            missing = b[index]
            for x in missing:
                self.df[col][row] = x
                self.solved = self.SodukuAlgo(self.df)
                if self.solved:
                    self.signals.result.emit(self.df)
                    self.signals.finished.emit()
                    break
                self.df = self.df_original.copy()
        if not self.solved:
            self.signals.result.emit(self.df_original)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Soduku()
    form.show()
    app.exec_()
