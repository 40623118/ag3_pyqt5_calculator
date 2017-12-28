# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .Ui_Dialog import Ui_Dialog
import math


class Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        '''以下為使用者自行編寫程式碼區'''
        self.display.setText('0')
        self.pendingAdditiveOperator = ''
        self.pendingMultiplicativeOperator = ''
        self.sumInMemory = 0.0
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.waitingForOperand = True
        number = [self.zero, self.one, self.two, self.three, self.four,
            self.five, self.six ,self.seven ,self.eight, self.nine]
        for i in number:
           i.clicked.connect(self.digitClicked)
        self.clearButton.clicked.connect(self.clear)
        self.clearAllButton.clicked.connect(self.clearAll)
        for button in [self.plusButton, self.minusButton]:
            button.clicked.connect(self.additiveOperatorClicked)
        for button in [self.timesButton, self.divisionButton]:
            button.clicked.connect(self.multiplicativeOperatorClicked)
        self.equalButton.clicked.connect(self.equalClicked)
        self.backspaceButton.clicked.connect(self.backspaceClicked)
        unaryOperator = [self.squareRootButton, self.powerButton,  self.reciprocalButton ]
        for i in unaryOperator:
            i.clicked.connect(self.unaryOperatorClicked)
            
    def digitClicked(self):
        '''
        使用者按下數字鍵, 必須能夠累積顯示該數字
        當顯示幕已經為 0, 再按零不會顯示 00, 而仍顯示 0 或 0.0
        
        '''
        button = self.sender()
        if self.display.text() == '0' and int(button.text())== 0.0:
            return
        if self.waitingForOperand:
            self.display.clear()
            self.waitingForOperand = False
        self.display.setText(self.display.text() + button.text())
    
    def unaryOperatorClicked(self):
        '''單一運算元按下後處理方法'''
        #pass
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())
 
        if clickedOperator == "Sqrt":
            if operand < 0.0:
                self.abortOperation()
                return
 
            result = math.sqrt(operand)
        elif clickedOperator == "X^2":
            result = math.pow(operand, 2.0)
        elif clickedOperator == "1/x":
            if operand == 0.0:
                self.abortOperation()
                return
 
            result = 1.0 / operand
 
        self.display.setText(str(result))
        self.waitingForOperand = True
    
    def additiveOperatorClicked(self):
        '''加或減按下後進行的處理方法'''
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())
        if self.pendingMultiplicativeOperator:
            '''
            計算：self.calculate(乘數或除數, 運算子)
            回傳 bool 以知道運算成功與否
            Python 文法：[if not 結果:] 當失敗時執行 self.abortOperation()。
            '''
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
            self.display.setText(str(self.factorSoFar))
            operand, self.factorSoFar = self.factorSoFar, 0.0
            self.pendingMultiplicativeOperator = ''
        if self.pendingAdditiveOperator:
            '''
            同上
            '''
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return
            self.display.setText(str(self.sumSoFar))
        else:
            self.sumSoFar = operand
        self.pendingAdditiveOperator = clickedOperator
        self.waitingForOperand = True
    
    def multiplicativeOperatorClicked(self):
        '''乘或除按下後進行的處理方法'''
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())
        if self.pendingMultiplicativeOperator:
            '''
            同加減法
            '''
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
            self.display.setText(str(self.factorSoFar))
        else:
            self.factorSoFar = operand
        self.pendingMultiplicativeOperator = clickedOperator
        self.waitingForOperand = True
    
    def equalClicked(self):
        '''等號按下後的處理方法'''
        operand = float(self.display.text())
        '''
        同乘除
        '''
        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ''
        '''
        同加減
        '''
        if self.pendingAdditiveOperator:
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return
            self.pendingAdditiveOperator = ''
        else:
            self.sumSoFar = operand
        self.display.setText(str(self.sumSoFar))
        self.sumSoFar = 0.0
        self.waitingForOperand = True
    
    def pointClicked(self):
        pass
    def changeSignClicked(self):
        pass
    def backspaceClicked(self):
        #pass
         #if self.wait:
            #return
        text = self.display.text()[:-1]
        if not text:
            text = '0'
            self.wait = True
        self.display.setText(text)

        
    def clear(self):
        '''清除鍵按下後的處理方法'''
        self.display.setText('0')
        self.wait = True
    
    def clearAll(self):
        '''全部清除鍵按下後的處理方法'''
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.pendingAdditiveOperator = ''
        self.pendingMultiplicativeOperator = ''
        self.display.setText('0')
        self.waitingForOperand = True
    
    def clearMemory(self):
        '''清除記憶體鍵按下後的處理方法'''
        pass
    
    def readMemory(self):
        '''讀取記憶體鍵按下後的處理方法'''
        pass
    
    def setMemory(self):
        '''設定記憶體鍵按下後的處理方法'''
        pass
    
    def addToMemory(self):
        '''放到記憶體鍵按下後的處理方法'''
        pass
    
    def createButton(self):
        ''' 建立按鍵處理方法, 以 Qt Designer 建立對話框時, 不需要此方法'''
        pass
    
    def abortOperation(self):   
        #pass
        self.clearAll()
        self.display.setText("####")
    
    def calculate(self, rightOperand, pendingOperator):
        '''計算'''
        if pendingOperator == "+":
            self.sumSoFar += rightOperand
        elif pendingOperator == "-":
            self.sumSoFar -= rightOperand
        elif pendingOperator == "*":
            self.factorSoFar *= rightOperand
        elif pendingOperator == "/":
            if rightOperand == 0.0:
                return False
            self.factorSoFar /= rightOperand
        return True
