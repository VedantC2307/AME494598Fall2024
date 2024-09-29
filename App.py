import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGroupBox, 
                             QRadioButton, QSlider, QStateMachine, QState, QStackedWidget, QGridLayout, QSpinBox)
from PyQt5.QtCore import Qt

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()

        # TCP Connect Section
        tcp_layout = QHBoxLayout()
        self.ip_label = QLabel('IP Address:')
        self.ip_edit = QLineEdit('localhost')
        self.port_label = QLabel('Port:')
        self.port_edit = QSpinBox()
        self.port_edit.setValue(12345)
        self.connect_btn = QPushButton('Connect')
        self.disconnect_btn = QPushButton('Disconnect')
        
        tcp_layout.addWidget(self.ip_label)
        tcp_layout.addWidget(self.ip_edit)
        tcp_layout.addWidget(self.port_label)
        tcp_layout.addWidget(self.port_edit)
        tcp_layout.addWidget(self.connect_btn)
        tcp_layout.addWidget(self.disconnect_btn)
        
        # Add to main layout
        main_layout.addLayout(tcp_layout)

        # Control Mode Section
        control_mode_group = QGroupBox('Control Mode')
        control_layout = QVBoxLayout()
        self.position_btn = QRadioButton('Position')
        self.velocity_btn = QRadioButton('Velocity')
        self.torque_btn = QRadioButton('Torque')
        self.value_edit = QLineEdit('0.00')
        self.send_btn = QPushButton('Send')

        control_layout.addWidget(self.position_btn)
        control_layout.addWidget(self.velocity_btn)
        control_layout.addWidget(self.torque_btn)
        control_layout.addWidget(QLabel('Value'))
        control_layout.addWidget(self.value_edit)
        control_layout.addWidget(self.send_btn)
        
        control_mode_group.setLayout(control_layout)
        main_layout.addWidget(control_mode_group)

        # Data Recording Section
        data_record_layout = QHBoxLayout()
        self.topic_name_label = QLabel('Topic Name:')
        self.topic_name_edit = QLineEdit()
        self.file_name_label = QLabel('File Name:')
        self.file_name_edit = QLineEdit()
        self.start_record_btn = QPushButton('Start')
        
        data_record_layout.addWidget(self.topic_name_label)
        data_record_layout.addWidget(self.topic_name_edit)
        data_record_layout.addWidget(self.file_name_label)
        data_record_layout.addWidget(self.file_name_edit)
        data_record_layout.addWidget(self.start_record_btn)
        
        main_layout.addLayout(data_record_layout)

        # Set main layout
        self.setLayout(main_layout)
        self.setWindowTitle('Converted MATLAB App')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
