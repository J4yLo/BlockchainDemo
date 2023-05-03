# Form implementation generated from reading ui file 'Home.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_scr_Main(object):
    def setupUi(self, scr_Main):
        scr_Main.setObjectName("scr_Main")
        scr_Main.resize(1098, 820)
        self.centralwidget = QtWidgets.QWidget(parent=scr_Main)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.listWidget = QtWidgets.QListWidget(parent=self.centralwidget)
        self.listWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.listWidget.setMaximumSize(QtCore.QSize(200, 16777215))
        self.listWidget.setObjectName("listWidget")
        self.gridLayout_2.addWidget(self.listWidget, 2, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 0, 1, 1, 1)
        self.fr_VisualArea = QtWidgets.QFrame(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fr_VisualArea.sizePolicy().hasHeightForWidth())
        self.fr_VisualArea.setSizePolicy(sizePolicy)
        self.fr_VisualArea.setMinimumSize(QtCore.QSize(700, 500))
        self.fr_VisualArea.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.fr_VisualArea.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.fr_VisualArea.setObjectName("fr_VisualArea")
        self.label_14 = QtWidgets.QLabel(parent=self.fr_VisualArea)
        self.label_14.setGeometry(QtCore.QRect(670, 10, 50, 50))
        self.label_14.setText("")
        self.label_14.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.label_14.setPixmap(QtGui.QPixmap("Assets/Images/Icons/Node_Icon_Valid.png"))
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.fr_VisualArea, 2, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 1, 1, 1, 1)
        self.tb_Overview = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tb_Overview.setMinimumSize(QtCore.QSize(0, 50))
        self.tb_Overview.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tb_Overview.setObjectName("tb_Overview")
        self.Overview = QtWidgets.QWidget()
        self.Overview.setObjectName("Overview")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.Overview)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lst_Overview = QtWidgets.QListWidget(parent=self.Overview)
        self.lst_Overview.setEnabled(True)
        self.lst_Overview.setObjectName("lst_Overview")
        self.verticalLayout_3.addWidget(self.lst_Overview)
        self.tb_Overview.addTab(self.Overview, "")
        self.Messages = QtWidgets.QWidget()
        self.Messages.setObjectName("Messages")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.Messages)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tbl_Messages = QtWidgets.QTableWidget(parent=self.Messages)
        self.tbl_Messages.setObjectName("tbl_Messages")
        self.tbl_Messages.setColumnCount(0)
        self.tbl_Messages.setRowCount(0)
        self.verticalLayout.addWidget(self.tbl_Messages)
        self.tb_Overview.addTab(self.Messages, "")
        self.tb_BlockChain = QtWidgets.QWidget()
        self.tb_BlockChain.setObjectName("tb_BlockChain")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tb_BlockChain)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tbl_Blockchain = QtWidgets.QTableView(parent=self.tb_BlockChain)
        self.tbl_Blockchain.setObjectName("tbl_Blockchain")
        self.verticalLayout_2.addWidget(self.tbl_Blockchain)
        self.tb_Overview.addTab(self.tb_BlockChain, "")
        self.Nodes = QtWidgets.QWidget()
        self.Nodes.setObjectName("Nodes")
        self.gridLayout = QtWidgets.QGridLayout(self.Nodes)
        self.gridLayout.setObjectName("gridLayout")
        self.chk_AttackerNode = QtWidgets.QCheckBox(parent=self.Nodes)
        self.chk_AttackerNode.setObjectName("chk_AttackerNode")
        self.gridLayout.addWidget(self.chk_AttackerNode, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.Nodes)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.txt_NodeName = QtWidgets.QTextEdit(parent=self.Nodes)
        self.txt_NodeName.setObjectName("txt_NodeName")
        self.gridLayout.addWidget(self.txt_NodeName, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.Nodes)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.Nodes)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 1, 1, 1)
        self.txt_NodeTrust = QtWidgets.QTextEdit(parent=self.Nodes)
        self.txt_NodeTrust.setObjectName("txt_NodeTrust")
        self.gridLayout.addWidget(self.txt_NodeTrust, 2, 1, 1, 1)
        self.btn_AddNode = QtWidgets.QPushButton(parent=self.Nodes)
        self.btn_AddNode.setMinimumSize(QtCore.QSize(0, 60))
        self.btn_AddNode.setObjectName("btn_AddNode")
        self.gridLayout.addWidget(self.btn_AddNode, 2, 2, 1, 1)
        self.tb_Overview.addTab(self.Nodes, "")
        self.Block = QtWidgets.QWidget()
        self.Block.setObjectName("Block")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.Block)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_7 = QtWidgets.QLabel(parent=self.Block)
        self.label_7.setObjectName("label_7")
        self.gridLayout_5.addWidget(self.label_7, 2, 0, 1, 1)
        self.txt_blkData = QtWidgets.QTextEdit(parent=self.Block)
        self.txt_blkData.setObjectName("txt_blkData")
        self.gridLayout_5.addWidget(self.txt_blkData, 2, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(parent=self.Block)
        self.label_6.setObjectName("label_6")
        self.gridLayout_5.addWidget(self.label_6, 0, 0, 1, 3)
        self.txt_NodeID = QtWidgets.QTextEdit(parent=self.Block)
        self.txt_NodeID.setObjectName("txt_NodeID")
        self.gridLayout_5.addWidget(self.txt_NodeID, 1, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(parent=self.Block)
        self.label_8.setObjectName("label_8")
        self.gridLayout_5.addWidget(self.label_8, 1, 0, 1, 1)
        self.btn_AddBlockToNode = QtWidgets.QPushButton(parent=self.Block)
        self.btn_AddBlockToNode.setObjectName("btn_AddBlockToNode")
        self.gridLayout_5.addWidget(self.btn_AddBlockToNode, 3, 2, 1, 1)
        self.tb_Overview.addTab(self.Block, "")
        self.ProofOfWork = QtWidgets.QWidget()
        self.ProofOfWork.setObjectName("ProofOfWork")
        self.pushButton = QtWidgets.QPushButton(parent=self.ProofOfWork)
        self.pushButton.setGeometry(QtCore.QRect(290, 20, 75, 51))
        self.pushButton.setObjectName("pushButton")
        self.txted_Hash = QtWidgets.QTextEdit(parent=self.ProofOfWork)
        self.txted_Hash.setGeometry(QtCore.QRect(10, 30, 261, 31))
        self.txted_Hash.setObjectName("txted_Hash")
        self.lbl_pwHash = QtWidgets.QLabel(parent=self.ProofOfWork)
        self.lbl_pwHash.setGeometry(QtCore.QRect(120, 10, 31, 16))
        self.lbl_pwHash.setObjectName("lbl_pwHash")
        self.lbl_pwHashDesc = QtWidgets.QLabel(parent=self.ProofOfWork)
        self.lbl_pwHashDesc.setGeometry(QtCore.QRect(80, 70, 121, 16))
        self.lbl_pwHashDesc.setObjectName("lbl_pwHashDesc")
        self.tb_Overview.addTab(self.ProofOfWork, "")
        self.Settings = QtWidgets.QWidget()
        self.Settings.setObjectName("Settings")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.Settings)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.txt_DefultTrust = QtWidgets.QTextEdit(parent=self.Settings)
        self.txt_DefultTrust.setObjectName("txt_DefultTrust")
        self.gridLayout_6.addWidget(self.txt_DefultTrust, 1, 1, 1, 1)
        self.ckb_FaultTollerance = QtWidgets.QCheckBox(parent=self.Settings)
        self.ckb_FaultTollerance.setObjectName("ckb_FaultTollerance")
        self.gridLayout_6.addWidget(self.ckb_FaultTollerance, 1, 2, 1, 1)
        self.chk_PauseMining = QtWidgets.QCheckBox(parent=self.Settings)
        self.chk_PauseMining.setObjectName("chk_PauseMining")
        self.gridLayout_6.addWidget(self.chk_PauseMining, 1, 3, 1, 1)
        self.ckb_ProofofStake = QtWidgets.QCheckBox(parent=self.Settings)
        self.ckb_ProofofStake.setObjectName("ckb_ProofofStake")
        self.gridLayout_6.addWidget(self.ckb_ProofofStake, 0, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.Settings)
        self.label_4.setObjectName("label_4")
        self.gridLayout_6.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.Settings)
        self.label_5.setObjectName("label_5")
        self.gridLayout_6.addWidget(self.label_5, 2, 1, 1, 1)
        self.ckb_ProofofWork = QtWidgets.QCheckBox(parent=self.Settings)
        self.ckb_ProofofWork.setObjectName("ckb_ProofofWork")
        self.gridLayout_6.addWidget(self.ckb_ProofofWork, 2, 2, 1, 1)
        self.btn_applySettings = QtWidgets.QPushButton(parent=self.Settings)
        self.btn_applySettings.setObjectName("btn_applySettings")
        self.gridLayout_6.addWidget(self.btn_applySettings, 1, 5, 1, 1)
        self.tb_Overview.addTab(self.Settings, "")
        self.tb_malliciousFunctions = QtWidgets.QWidget()
        self.tb_malliciousFunctions.setObjectName("tb_malliciousFunctions")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tb_malliciousFunctions)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_13 = QtWidgets.QLabel(parent=self.tb_malliciousFunctions)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 1, 0, 1, 1)
        self.txt_BlockID = QtWidgets.QTextEdit(parent=self.tb_malliciousFunctions)
        self.txt_BlockID.setObjectName("txt_BlockID")
        self.gridLayout_3.addWidget(self.txt_BlockID, 1, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(parent=self.tb_malliciousFunctions)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 0, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(parent=self.tb_malliciousFunctions)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 5, 0, 1, 1)
        self.btn_ChangeBlock = QtWidgets.QPushButton(parent=self.tb_malliciousFunctions)
        self.btn_ChangeBlock.setObjectName("btn_ChangeBlock")
        self.gridLayout_3.addWidget(self.btn_ChangeBlock, 6, 1, 1, 1)
        self.txt_changeBlockData = QtWidgets.QTextEdit(parent=self.tb_malliciousFunctions)
        self.txt_changeBlockData.setObjectName("txt_changeBlockData")
        self.gridLayout_3.addWidget(self.txt_changeBlockData, 5, 1, 1, 1)
        self.tb_Overview.addTab(self.tb_malliciousFunctions, "")
        self.tb_StepThrough = QtWidgets.QWidget()
        self.tb_StepThrough.setObjectName("tb_StepThrough")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tb_StepThrough)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_9 = QtWidgets.QLabel(parent=self.tb_StepThrough)
        self.label_9.setObjectName("label_9")
        self.gridLayout_4.addWidget(self.label_9, 1, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(parent=self.tb_StepThrough)
        self.label_10.setObjectName("label_10")
        self.gridLayout_4.addWidget(self.label_10, 0, 3, 1, 1)
        self.txt_addBlockToAllNodes = QtWidgets.QTextEdit(parent=self.tb_StepThrough)
        self.txt_addBlockToAllNodes.setObjectName("txt_addBlockToAllNodes")
        self.gridLayout_4.addWidget(self.txt_addBlockToAllNodes, 1, 3, 1, 1)
        self.btn_AddBlock = QtWidgets.QPushButton(parent=self.tb_StepThrough)
        self.btn_AddBlock.setObjectName("btn_AddBlock")
        self.gridLayout_4.addWidget(self.btn_AddBlock, 2, 3, 1, 1)
        self.btn_Mine = QtWidgets.QPushButton(parent=self.tb_StepThrough)
        self.btn_Mine.setMinimumSize(QtCore.QSize(0, 60))
        self.btn_Mine.setObjectName("btn_Mine")
        self.gridLayout_4.addWidget(self.btn_Mine, 1, 4, 1, 1)
        self.tb_Overview.addTab(self.tb_StepThrough, "")
        self.tb_About = QtWidgets.QWidget()
        self.tb_About.setObjectName("tb_About")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tb_About)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_19 = QtWidgets.QLabel(parent=self.tb_About)
        self.label_19.setMaximumSize(QtCore.QSize(50, 50))
        self.label_19.setText("")
        self.label_19.setPixmap(QtGui.QPixmap("../../Demo/BlockchainDemo/Assets/Images/Icons/Node_Icon_Primary_Attacker.png"))
        self.label_19.setObjectName("label_19")
        self.gridLayout_7.addWidget(self.label_19, 2, 1, 1, 1)
        self.label_18 = QtWidgets.QLabel(parent=self.tb_About)
        self.label_18.setMaximumSize(QtCore.QSize(50, 50))
        self.label_18.setText("")
        self.label_18.setPixmap(QtGui.QPixmap("../../Demo/BlockchainDemo/Assets/Images/Icons/Node_Icon_Primary.png"))
        self.label_18.setObjectName("label_18")
        self.gridLayout_7.addWidget(self.label_18, 2, 4, 1, 1)
        self.label_17 = QtWidgets.QLabel(parent=self.tb_About)
        self.label_17.setMaximumSize(QtCore.QSize(50, 50))
        self.label_17.setText("")
        self.label_17.setPixmap(QtGui.QPixmap("../../Demo/BlockchainDemo/Assets/Images/Icons/Node_Icon__Attacker.png"))
        self.label_17.setObjectName("label_17")
        self.gridLayout_7.addWidget(self.label_17, 0, 1, 1, 1)
        self.label_21 = QtWidgets.QLabel(parent=self.tb_About)
        self.label_21.setText("")
        self.label_21.setPixmap(QtGui.QPixmap("../../Demo/BlockchainDemo/Assets/Images/Icons/Node_Icon_Valid.png"))
        self.label_21.setObjectName("label_21")
        self.gridLayout_7.addWidget(self.label_21, 0, 4, 1, 1)
        self.label_25 = QtWidgets.QLabel(parent=self.tb_About)
        self.label_25.setMaximumSize(QtCore.QSize(150, 50))
        self.label_25.setObjectName("label_25")
        self.gridLayout_7.addWidget(self.label_25, 0, 5, 1, 1)
        self.label_20 = QtWidgets.QLabel(parent=self.tb_About)
        self.label_20.setMaximumSize(QtCore.QSize(50, 50))
        self.label_20.setText("")
        self.label_20.setPixmap(QtGui.QPixmap("../../Demo/BlockchainDemo/Assets/Images/Icons/Node_Icon_Selected.png"))
        self.label_20.setObjectName("label_20")
        self.gridLayout_7.addWidget(self.label_20, 0, 6, 1, 1)
        self.label_24 = QtWidgets.QLabel(parent=self.tb_About)
        self.label_24.setMaximumSize(QtCore.QSize(150, 50))
        self.label_24.setObjectName("label_24")
        self.gridLayout_7.addWidget(self.label_24, 2, 5, 1, 1)
        self.label_22 = QtWidgets.QLabel(parent=self.tb_About)
        self.label_22.setMaximumSize(QtCore.QSize(150, 50))
        self.label_22.setObjectName("label_22")
        self.gridLayout_7.addWidget(self.label_22, 2, 3, 1, 1)
        self.label_23 = QtWidgets.QLabel(parent=self.tb_About)
        self.label_23.setMaximumSize(QtCore.QSize(150, 50))
        self.label_23.setObjectName("label_23")
        self.gridLayout_7.addWidget(self.label_23, 0, 3, 1, 1)
        self.label_26 = QtWidgets.QLabel(parent=self.tb_About)
        self.label_26.setObjectName("label_26")
        self.gridLayout_7.addWidget(self.label_26, 0, 7, 1, 1)
        self.tb_Overview.addTab(self.tb_About, "")
        self.gridLayout_2.addWidget(self.tb_Overview, 5, 0, 1, 2)
        scr_Main.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=scr_Main)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1098, 22))
        self.menubar.setObjectName("menubar")
        self.menuFIle = QtWidgets.QMenu(parent=self.menubar)
        self.menuFIle.setObjectName("menuFIle")
        scr_Main.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=scr_Main)
        self.statusbar.setObjectName("statusbar")
        scr_Main.setStatusBar(self.statusbar)
        self.actionHome = QtGui.QAction(parent=scr_Main)
        self.actionHome.setObjectName("actionHome")
        self.actionSave = QtGui.QAction(parent=scr_Main)
        self.actionSave.setObjectName("actionSave")
        self.actionReset = QtGui.QAction(parent=scr_Main)
        self.actionReset.setObjectName("actionReset")
        self.menuFIle.addAction(self.actionHome)
        self.menuFIle.addAction(self.actionSave)
        self.menuFIle.addAction(self.actionReset)
        self.menubar.addAction(self.menuFIle.menuAction())

        self.retranslateUi(scr_Main)
        self.tb_Overview.setCurrentIndex(9)
        QtCore.QMetaObject.connectSlotsByName(scr_Main)

    def retranslateUi(self, scr_Main):
        _translate = QtCore.QCoreApplication.translate
        scr_Main.setWindowTitle(_translate("scr_Main", "Decentralised Sec"))
        self.label_16.setText(_translate("scr_Main", "Network Run Time:"))
        self.label_15.setText(_translate("scr_Main", "00:00:00:00"))
        self.tb_Overview.setTabText(self.tb_Overview.indexOf(self.Overview), _translate("scr_Main", "Network Overview"))
        self.tb_Overview.setTabText(self.tb_Overview.indexOf(self.Messages), _translate("scr_Main", "Messages"))
        self.tb_Overview.setTabText(self.tb_Overview.indexOf(self.tb_BlockChain), _translate("scr_Main", "BlockChain"))
        self.chk_AttackerNode.setText(_translate("scr_Main", "Attacker Node?"))
        self.label.setText(_translate("scr_Main", "Node Name:"))
        self.label_2.setText(_translate("scr_Main", "Trust:"))
        self.label_3.setText(_translate("scr_Main", "Leave Blank To Apply Defult"))
        self.btn_AddNode.setText(_translate("scr_Main", "Add Node"))
        self.tb_Overview.setTabText(self.tb_Overview.indexOf(self.Nodes), _translate("scr_Main", "Nodes"))
        self.label_7.setText(_translate("scr_Main", "DATA:"))
        self.label_6.setText(_translate("scr_Main", "Add Block To Node"))
        self.label_8.setText(_translate("scr_Main", "Node ID:"))
        self.btn_AddBlockToNode.setText(_translate("scr_Main", "Add To Node"))
        self.tb_Overview.setTabText(self.tb_Overview.indexOf(self.Block), _translate("scr_Main", "Block"))
        self.pushButton.setText(_translate("scr_Main", "Submit"))
        self.lbl_pwHash.setText(_translate("scr_Main", "HASH"))
        self.lbl_pwHashDesc.setText(_translate("scr_Main", "Leave empty for defult"))
        self.tb_Overview.setTabText(self.tb_Overview.indexOf(self.ProofOfWork), _translate("scr_Main", "Proof Of Work"))
        self.ckb_FaultTollerance.setText(_translate("scr_Main", "Byzantine Fault Tolerance "))
        self.chk_PauseMining.setText(_translate("scr_Main", "Automatic Mining"))
        self.ckb_ProofofStake.setText(_translate("scr_Main", "Proof Of Stake"))
        self.label_4.setText(_translate("scr_Main", "Defult Trust:"))
        self.label_5.setText(_translate("scr_Main", "Leave Empty to Apply Defult"))
        self.ckb_ProofofWork.setText(_translate("scr_Main", "Proof Of Work"))
        self.btn_applySettings.setText(_translate("scr_Main", "APPLY"))
        self.tb_Overview.setTabText(self.tb_Overview.indexOf(self.Settings), _translate("scr_Main", "Settings"))
        self.label_13.setText(_translate("scr_Main", "Block ID"))
        self.label_11.setText(_translate("scr_Main", "Change Block"))
        self.label_12.setText(_translate("scr_Main", "DATA:"))
        self.btn_ChangeBlock.setText(_translate("scr_Main", "Change Block"))
        self.tb_Overview.setTabText(self.tb_Overview.indexOf(self.tb_malliciousFunctions), _translate("scr_Main", "Attack Network"))
        self.label_9.setText(_translate("scr_Main", "DATA:"))
        self.label_10.setText(_translate("scr_Main", "Broadcast Block To all Nodes"))
        self.btn_AddBlock.setText(_translate("scr_Main", "Add Block"))
        self.btn_Mine.setText(_translate("scr_Main", "Mine"))
        self.tb_Overview.setTabText(self.tb_Overview.indexOf(self.tb_StepThrough), _translate("scr_Main", "Advanced"))
        self.label_25.setText(_translate("scr_Main", "- Normal Node"))
        self.label_24.setText(_translate("scr_Main", "- Primary Node"))
        self.label_22.setText(_translate("scr_Main", "- Primary Attacker Node"))
        self.label_23.setText(_translate("scr_Main", "- Atacker Node"))
        self.label_26.setText(_translate("scr_Main", "- Selected Node"))
        self.tb_Overview.setTabText(self.tb_Overview.indexOf(self.tb_About), _translate("scr_Main", "About"))
        self.menuFIle.setTitle(_translate("scr_Main", "FIle"))
        self.actionHome.setText(_translate("scr_Main", "Home"))
        self.actionSave.setText(_translate("scr_Main", "Save"))
        self.actionReset.setText(_translate("scr_Main", "Reset"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    scr_Main = QtWidgets.QMainWindow()
    ui = Ui_scr_Main()
    ui.setupUi(scr_Main)
    scr_Main.show()
    sys.exit(app.exec())
