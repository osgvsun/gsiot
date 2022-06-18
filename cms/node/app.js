var express = require('express');
var requestSync = require('sync-request');
var program = require('commander'); 
var url = require('url');
var paths = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var http = require('http');
var fs = require('fs');
// var https = require('https');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var config=require("./config.js");
// var expressJwt = require("express-jwt");
// var jwt = require("jsonwebtoken");
// var shortid = require("shortid");
var submodule={}
submodule.list=[]
var ulinkPath=[]
var app = express();
var webport = '9521';
app.use(express.json())

// const SECRET = "fdfhfjdfdjfdjerwrereresaassa2dd@ddds"

// // app.get('/', async(req, res) => {
// //   res.send('ok')
// // })

// app.get('/api', (req, res) => res.send('Hello World!'))

// // 从MongoDB数据库express-auth中的User表查询所有的用户信息
// app.get('/api/users', async (req, res) => {
//     const users = await User.find()
//     res.send(users)
// })

// app.post('/api/register', async (req, res) => {
//     // console.log(req.body)
//     // 在MongoDB数据库表USer中新增一个用户
//     const user = await User.create({
//         username: req.body.username,
//         password: req.body.password,
//     })

//     // res.send('register')
//     res.send(user)
// })

// app.post('/api/login', async (req, res) => {
//     // res.send('login')
//     // 1.看用户是否存在
//     const user = await User.findOne({
//         username: req.body.username
//     })
//     if (!user) {
//         return res.status(422).send({
//             message: '用户名不存在'
//         })
//     }
//     // 2.用户如果存在，则看密码是否正确
//     const isPasswordValid = require('bcryptjs').compareSync(
//         req.body.password,
//         user.password
//     )
//     if (!isPasswordValid) {
//         // 密码无效
//         return res.status(422).send({
//             message: '密码无效'
//         })
//     }
//     // 生成token
//     const token = jwt.sign({
//         id: String(user._id),
//     }, SECRET)

//     res.send({
//         user,
//         token
//     })
// })

// // 中间件：验证授权
// const auth = async (req, res, next) => {
//     // 获取客户端请求头的token
//     const rawToken = String(req.headers.authorization).split(' ').pop()
//     const tokenData = jwt.verify(rawToken, SECRET)
//     //  console.log(tokenData)
//     // 获取用户id
//     const id = tokenData.id;
//     //  const user = await User.findById(id)
//     req.user = await User.findById(id)
//     next()
// }

// app.get('/api/profile', auth, async (req, res) => {
//     res.send(req.user)
// })
Array.prototype.Add = function(value) {this.push(value);return this;};
Array.prototype.ForEach = function(fn) {
    for(index=0;index<this.length;index++){if(fn(this[index],index))break;}
};
Date.prototype.Format = function (fmt) { var o = { "M+": this.getMonth() + 1, "d+": this.getDate(), "h+": this.getHours(), "m+": this.getMinutes(), "s+": this.getSeconds(), "q+": Math.floor((this.getMonth() + 3) / 3), "S": this.getMilliseconds() }; if (/(y+)/.test(fmt)){fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));} for (var k in o){ 　　　　if (new RegExp("(" + k + ")").test(fmt)){ 　　　　　　fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));}} return fmt; };

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
var http_server = http.createServer(app);
http_server.listen(webport, function () {
    console.log('HTTP Server is running on: http://localhost:%s', webport);
    if(process.argv.length>2){process.argv.forEach(function(item,index){if(index>=2)submodule.list.Add(item);});}
    else{submodule.list=["webfs"];};
    submodule.list.forEach(function(item,index){
        app.use("/"+item,require('./router/'+item))
        // submodule[item]=require(__dirname+'/router/'+item+'.js');
        // submodule[item](app);
    });
});

module.exports = app;
