//创建一个路由就要先实例化express下创建路由的方法
const express=require('express');
var child = require('child_process');
const router=express.Router();//注意这里的router是方法，需要括号
const jwt = require("jsonwebtoken");
const request = require("request");
var requestSync = require('sync-request');
const config=require("../config.js")

router.get('/', (req, res) =>{
    
});
router.get('/:adapter', (req, res) =>{
    
});
router.get('/:adapter/ScanAP', (req, res) =>{
    
});
router.post('/:adapter/ConnAP', (req, res) =>{
    
});
router.post('(*)', (req, res)=> {
    
});
//路由写完了，现在可以把该数据库返回到操作层了
module.exports=router;