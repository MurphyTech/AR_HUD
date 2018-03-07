var http = require('http').createServer(handler); //Require http server, and create server with function jandler()
var fs = require('fs'); // reuire filesystem module

http.listen(8088); // listen to port 8088

function handler (req, res) {
	fs.readFile(__dirname + '/public/index.html', function(err, data) { //read file index.html in public folder
		if (err) {
			res.writeHead(404, {'Content-Type': 'text/html'}); //display 404 error
			return res.end("404 - Not Found");
		}
		res.writeHead(200, {'Content-Type': 'text/html'}); //write HTML
		res.write(data); //write data from index.html
		console.log(data);
		return res.end();
	});
}
