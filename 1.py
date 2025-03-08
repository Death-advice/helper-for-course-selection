from PySide6.QtWidgets import QApplication,QMainWindow,QPushButton,QPlainTextEdit,QMessageBox
import requests
import loginfunc
def loginfosub():
    username=log_username.toPlainText()
    password=log_password.toPlainText()
    resp=loginfunc.login(username,password)
    QMessageBox.about(window,f'test',f'{username}\n,{password}\n,{resp}')

app=QApplication([])
window=QMainWindow()
window.resize(800,600)
window.setWindowTitle("course select")

log_username=QPlainTextEdit(window)
log_username.move(200,200)
log_username.setPlaceholderText("账号")
log_password=QPlainTextEdit(window)
log_password.setPlaceholderText("密码")
log_password.move(200,300)

log_button=QPushButton("登录",window)
log_button.move(360,400)
log_button.clicked.connect(loginfosub)

window.show()
app.exec()