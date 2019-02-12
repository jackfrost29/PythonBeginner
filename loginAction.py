from flask import Flask, request, render_template
import cgitb; cgitb.enable()
import cgi
import sys

form = cgi.FieldStorage()
name = form.getvalue('userName')

render_template('loginSuccess.html', user=name)