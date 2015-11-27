#!"C:\Python27\python.exe"

import cgitb
import cgi
import sqlite3
import Cookie
import datetime
import os

cgitb.enable()

#Retrieve the username and password from the HTML field
form = cgi.FieldStorage()
thread = form['thread'].value

#initialize use of the database
conn = sqlite3.connect('users.db')
c = conn.cursor()

firstname = ""
lastname = ""
image = ""

def redirect():
	print 'Content-Type: text/html'
	print

	# print the HTTP body, which is the HTML file representing lecture1.html

	print '''
	<html>
	<head>
		<title>
			Redirecting... | iGG
		</title>
		<link rel="stylesheet" type="text/css" href="../main.css">
		<link rel="shortcut icon" href="../img/icons/favicon.ico" type="image/x-icon">
		<link rel="icon" href="../img/icons/favicon.ico" type="image/x-icon">
		
		<script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
		<script type="text/javascript">
			function loader(){
				window.location.replace("../");
			}
			window.onload = loader

		$(document).ready(function(){

			$.ajax({

				url: "/cgi-bin/html-banner.py",

				data: {
				},

				type: "GET",

				dataType: "html",

				success: function(data){

					$("div.banner").html(data);

					$("#username").focus();

				}

			});

		});
		</script>

		<script src="/js-bin/client-login-logout.js" type="text/javascript">
		</script>
	</head>

	<body>
		<div class="wrapper">
			<div class="banner">
			</div>

			<div class="mainpage">
			</div>
		</div>
		
		<div class="footer" xmlns:dc="http://purl.org/dc/elements/1.1/">
			<img src="../img/icons/hr.png" style="vertical-align:middle">
			<p id="copyright" property="dc:rights">&copy;
				<span property="dc:dateCopyrighted">2015</span>
				<span property="dc:publisher">Adeeb Sheikh</span>
			</p>
		</div>

	</body>
	</html>'''

def viewThread():
	proceed = False

	username = ""
	title = ""
	date = ""
	body = ""
	for r in c.execute('select * from grammars'):
		proceed = False
		grammarid = r[0]

		if grammarid == thread:
			proceed = True
			username = r[1].decode('hex')
			date = r[2]
			body = r[3].decode('hex')
			title = r[4].decode('hex')

	if proceed:
		#Find the user and retrieve the values
		#NOTE: this script doesn't really DO anything if the user doesn't exist and HAS a cookie with a matching username

		firstname = ""
		lastname = ""
		image = ""

		for b in c.execute('select * from accounts where username=?', [username.encode('hex')]):
			firstname = b[1].decode('hex')
			lastname = b[2].decode('hex')
			image = b[3].decode('hex')

		print 'Content-Type: text/html'
		print

		print '''
			<html>
			<head>
				<title>
						''' + title + ''' | iGG
				</title>
				<link rel="stylesheet" type="text/css" href="../main.css">
				<link rel="shortcut icon" href="../img/icons/favicon.ico" type="image/x-icon">
				<link rel="icon" href="../img/icons/favicon.ico" type="image/x-icon">
				
				<script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
				<script>
					$(document).ready(function(){

						$.ajax({

							url: "/cgi-bin/html-banner.py",

							data: {
							},

							type: "GET",

							dataType: "html",

							success: function(data){

								$("div.banner").html(data);

							}

						});

					});
				</script>

				<script src="/js-bin/client-login-logout.js" type="text/javascript">
				</script>
			</head>
			<body>
				<div class="wrapper">
					<div class="banner">
					</div>

					<div class="mainpage">
						<table>
							<tr>
								<td>
									<div id="parent">
										<table>
											<tr>
												<td>
													<a href="/users/''' + username + '''">
														<div class="circle-cropper">
															<img src="''' + image + '''" class="rounded" />
														</div>
													</a>
												</td>

												<td>
													<a href="/threads/''' + thread + '''" style='text-decoration:none;color:black;'>
														<h1>
															''' + title + '''
														</h1>
													</a>
													
													<h2>
														<a href="/users/''' + username + '''" style='text-decoration:none;color:black;'>''' + username + '''</a>
													</h2>
												</td>
											</tr>

											<tr>
												<td>
												</td>

												<td>
													<p style="white-space:pre-wrap;">''' + body + '''</p>
												</td>
											</tr>

											<tr>
												<td>
												</td>

												<td style="opacity: 0.6;">
													''' + date + '''
												</td>
											</tr>
										</table>
									</div>
								</td>
							</tr>'''

		parent = thread

		while proceed:
			for a in c.execute('select * from comments'):
				proceed = False
			
				if parent == a[4]:
					parent = a[0]
					proceed = True
					username = a[1].decode('hex')
					date = a[2]
					body = a[3].decode('hex')
					break
			
			if proceed:
				print '''<tr>
							<td>
								<div class="comment">
									<table>
										<tr>
											<td>''' + '''
												<a href="/users/''' + username + '''" style="text-decoration:none;color:black;">
													<div class="circle-cropper">
														<img src="''' + image + '''" class="rounded" />
													</div>
												</a>
											</td>

											<td>
												<a href="/users/''' + username + '''" style="text-decoration:none;color:black;">
													<h2>
														''' + username + '''
													</h2>
												</a>
											</td>

										<tr>
											<td>
											</td>

											<td>
												<p style="white-space:pre-wrap;">''' + body + '''</p>
											</td>
										</tr>
										
										<tr>
											<td>
											</td>

											<td style="opacity: 0.6;">
												''' + date + '''
											</td>
										</tr>
									</table>
								</div>
							</td>
						</tr>'''
				
		print '''
						</table>
					</div>
				</div>

				<div class="footer" xmlns:dc="http://purl.org/dc/elements/1.1/">
					<img src="/img/icons/hr.png" style="vertical-align:middle">
					<p id="copyright" property="dc:rights">&copy;
						<span property="dc:dateCopyrighted">2015</span>
						<span property="dc:publisher">Adeeb Sheikh</span>
					</p>
				</div>
			</body>
		</html>'''
	else:
		redirect()

#Checks if there's a cookie already
stored_cookie_string = os.environ.get('HTTP_COOKIE')
#If not, it's a bad login!
if not stored_cookie_string:
	viewThread()
#Otherwise, check the cookie
else:
	cookie = Cookie.SimpleCookie(stored_cookie_string)
	#If the cookie is 'username'
	if 'username' in cookie:
		username = ""
		for r in c.execute('select * from loggedin where sessionid=?', [cookie['username'].value]):
			username = r[1].decode('hex')
		#If the username submitted in the form is on the cookie
		viewThread()
	else:
		viewThread()

conn.close()