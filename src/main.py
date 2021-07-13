from PySide2.QtWidgets import QApplication
from src.StartWidget import StartWidget
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    StartWidget = StartWidget()
    StartWidget.show()
    sys.exit(app.exec_())
