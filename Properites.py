# Form implementation generated from reading ui file 'Properties.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Properties(object):
    def setupUi(self, Properties):
        Properties.setObjectName("Properties")
        Properties.resize(407, 559)
        self.centralwidget = QtWidgets.QWidget(parent=Properties)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.prp_NodeName = QtWidgets.QLabel(parent=self.frame)
        self.prp_NodeName.setGeometry(QtCore.QRect(60, 0, 331, 51))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prp_NodeName.sizePolicy().hasHeightForWidth())
        self.prp_NodeName.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.prp_NodeName.setFont(font)
        self.prp_NodeName.setObjectName("prp_NodeName")
        self.label = QtWidgets.QLabel(parent=self.frame)
        self.label.setGeometry(QtCore.QRect(0, 0, 51, 51))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Assets/Images/Icons/Node_Icon_Valid.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 21, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lbl_prop_ID = QtWidgets.QLabel(parent=self.frame)
        self.lbl_prop_ID.setGeometry(QtCore.QRect(40, 50, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.lbl_prop_ID.setFont(font)
        self.lbl_prop_ID.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.lbl_prop_ID.setScaledContents(False)
        self.lbl_prop_ID.setObjectName("lbl_prop_ID")
        self.label_3 = QtWidgets.QLabel(parent=self.frame)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lbl_prop_Type = QtWidgets.QLabel(parent=self.frame)
        self.lbl_prop_Type.setGeometry(QtCore.QRect(60, 80, 331, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_prop_Type.setFont(font)
        self.lbl_prop_Type.setObjectName("lbl_prop_Type")
        self.label_4 = QtWidgets.QLabel(parent=self.frame)
        self.label_4.setGeometry(QtCore.QRect(10, 105, 49, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.lbl_prop_Trust = QtWidgets.QLabel(parent=self.frame)
        self.lbl_prop_Trust.setGeometry(QtCore.QRect(60, 100, 321, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_prop_Trust.setFont(font)
        self.lbl_prop_Trust.setObjectName("lbl_prop_Trust")
        self.label_5 = QtWidgets.QLabel(parent=self.frame)
        self.label_5.setGeometry(QtCore.QRect(10, 130, 111, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setStrikeOut(False)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.lbl_prop_time = QtWidgets.QLabel(parent=self.frame)
        self.lbl_prop_time.setGeometry(QtCore.QRect(110, 130, 271, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_prop_time.setFont(font)
        self.lbl_prop_time.setObjectName("lbl_prop_time")
        self.label_6 = QtWidgets.QLabel(parent=self.frame)
        self.label_6.setGeometry(QtCore.QRect(10, 170, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.lbl_prop_networkTime = QtWidgets.QLabel(parent=self.frame)
        self.lbl_prop_networkTime.setGeometry(QtCore.QRect(220, 170, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_prop_networkTime.setFont(font)
        self.lbl_prop_networkTime.setObjectName("lbl_prop_networkTime")
        self.verticalLayout.addWidget(self.frame)
        self.tb_Properties = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tb_Properties.setObjectName("tb_Properties")
        self.tb_prop_Messages = QtWidgets.QWidget()
        self.tb_prop_Messages.setObjectName("tb_prop_Messages")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tb_prop_Messages)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tbl_prop_msgs = QtWidgets.QTableView(parent=self.tb_prop_Messages)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbl_prop_msgs.sizePolicy().hasHeightForWidth())
        self.tbl_prop_msgs.setSizePolicy(sizePolicy)
        self.tbl_prop_msgs.setObjectName("tbl_prop_msgs")
        self.verticalLayout_2.addWidget(self.tbl_prop_msgs)
        self.tb_Properties.addTab(self.tb_prop_Messages, "")
        self.prop_tb_Activity = QtWidgets.QWidget()
        self.prop_tb_Activity.setObjectName("prop_tb_Activity")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.prop_tb_Activity)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tbl_prop_Activity = QtWidgets.QTableView(parent=self.prop_tb_Activity)
        self.tbl_prop_Activity.setObjectName("tbl_prop_Activity")
        self.verticalLayout_3.addWidget(self.tbl_prop_Activity)
        self.tb_Properties.addTab(self.prop_tb_Activity, "")
        self.prop_tb_Blockchain = QtWidgets.QWidget()
        self.prop_tb_Blockchain.setObjectName("prop_tb_Blockchain")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.prop_tb_Blockchain)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tbl_prop_Blockchain = QtWidgets.QTableWidget(parent=self.prop_tb_Blockchain)
        self.tbl_prop_Blockchain.setObjectName("tbl_prop_Blockchain")
        self.tbl_prop_Blockchain.setColumnCount(0)
        self.tbl_prop_Blockchain.setRowCount(0)
        self.verticalLayout_4.addWidget(self.tbl_prop_Blockchain)
        self.tb_Properties.addTab(self.prop_tb_Blockchain, "")
        self.verticalLayout.addWidget(self.tb_Properties)
        Properties.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=Properties)
        self.statusbar.setObjectName("statusbar")
        Properties.setStatusBar(self.statusbar)

        self.retranslateUi(Properties)
        self.tb_Properties.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Properties)

    def retranslateUi(self, Properties):
        _translate = QtCore.QCoreApplication.translate
        Properties.setWindowTitle(_translate("Properties", "Properties"))
        self.prp_NodeName.setText(_translate("Properties", "Node"))
        self.label_2.setText(_translate("Properties", "ID:"))
        self.lbl_prop_ID.setText(_translate("Properties", "0"))
        self.label_3.setText(_translate("Properties", "Type:"))
        self.lbl_prop_Type.setText(_translate("Properties", "Primary?"))
        self.label_4.setText(_translate("Properties", "Trust:"))
        self.lbl_prop_Trust.setText(_translate("Properties", "Trust Value"))
        self.label_5.setText(_translate("Properties", "Time Added:"))
        self.lbl_prop_time.setText(_translate("Properties", "Time"))
        self.label_6.setText(_translate("Properties", "Time Added (ntw elapsed):"))
        self.lbl_prop_networkTime.setText(_translate("Properties", "Ntw Time"))
        self.tb_Properties.setTabText(self.tb_Properties.indexOf(self.tb_prop_Messages), _translate("Properties", "Messages"))
        self.tb_Properties.setTabText(self.tb_Properties.indexOf(self.prop_tb_Activity), _translate("Properties", "Activity"))
        self.tb_Properties.setTabText(self.tb_Properties.indexOf(self.prop_tb_Blockchain), _translate("Properties", "BlockChain"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Properties = QtWidgets.QMainWindow()
    ui = Ui_Properties()
    ui.setupUi(Properties)
    Properties.show()
    sys.exit(app.exec())