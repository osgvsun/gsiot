//创建一个路由就要先实例化express下创建路由的方法
const express=require('express');
var child = require('child_process');
const router=express.Router();//注意这里的router是方法，需要括号
const jwt = require("jsonwebtoken");
const request = require("request");
var requestSync = require('sync-request');
const fs = require('fs');
const paths = require('path');
const url = require('url');
const config=require("../config.js")
let webroot=config.webfs.webroot;
let exts=['.lnk','.ulnk']
let ulinkPath=[]

child.exec('find '+config.webfs.webroot+' -name conn.ulnk', function(err, sto) {sto.split("\n").forEach(function(item){if(item!="")ulinkPath.Add(paths.dirname(item));});console.log(ulinkPath);})
var httpClient=function(url,header,params){
    var options = {};if(header)options.headers=header;if(params)options.form=params;
    console.log(url,header)
    return requestSync('GET',url,options).getBody('utf-8').toString();
}
router.get('(*)', (req, res) =>{
    let path=webroot+req.params[0]
    // console.log(req.query)
    let stats=err=connFile=resData=rURL=null;
    let ext=paths.extname(path)
    if(fs.existsSync(path)){
        stats=fs.statSync(path)
        if(stats.isFile()){
            if(exts.indexOf(ext)==-1)res.send({code:200,result:{file:path,data:fs.readFileSync(path, "utf-8")}})
            else if(ext==".ulnk" && paths.basename(path)!="conn.ulnk"){
                //如果是ulnk文件，查找是否有conn.ulnk，如果没有，则寻找上级
                if(!(fs.existsSync(paths.dirname(path)+"/conn.ulnk"))){ulinkPath.forEach(function(item){if(paths.dirname(path).indexOf(item)!=-1)connFile=item+"/conn.ulnk";})}
                else connFile=paths.dirname(path)+"/conn.ulnk";
                conn=JSON.parse(fs.readFileSync(connFile, "utf-8"))
                file=JSON.parse(fs.readFileSync(path, "utf-8"))
                
            }
        }else if(stats.isDirectory()){
            splitpath="/webfs"+path.replace(webroot,"");
            subfile=[],subfolder=[]
            fs.readdirSync(path).forEach((name)=>{
                ext=fs.statSync(path+name).isFile()?(paths.extname(name)==""?"file":paths.extname(name)):"dir";
                data={
                    name:splitpath+name,
                    ext:ext,
                    accessdate:stats.atime.Format("yyyy-MM-dd hh:mm:ss"),
                    modifydate:stats.mtime,
                    mode:stats.mode,
                    edit:"",show:"",delete:"",rename:""
                };
                if(ext=="dir"){
                    data.name+="/"
                    data.access=path.replace(webroot,"")+name+"/"
                    subfolder.Add(data)
                }else{
                    data.access=(path.replace(webroot,"")+name)
                    data.size=stats.size
                    
                    
                    if(ext==".md"){
                        data.edit="/edit/markdown/edit.html?file="+splitpath+name;
                        data.show="/edit/markdown/show.html?file="+splitpath+name;
                    }
                    // console.log(JSON.stringify(data,null,4))
                    subfile.Add(data);
                }
            })
            resData={code:200,result:{parent:paths.dirname(path)+"/",webroot:webroot,folder:path,subfolder:subfolder,subfile:subfile}}
        }
    }else{
        console.log(paths.dirname(path)+"/conn.ulnk",fs.existsSync(paths.dirname(path)+"/conn.ulnk"));
        if(fs.existsSync(paths.dirname(path)+"/conn.ulnk")==0){
            ulinkPath.reverse().forEach(function(item){
                console.log(paths.dirname(path),item,paths.dirname(path).indexOf(item));
                if(paths.dirname(path).indexOf(item)!=-1){
                    if(!connFile){
                        connFile=item+"/conn.ulnk";rURL=path.replace(item,"")
                    }
                }
            })
        }
        if(connFile!=null){
            conndata=JSON.parse(fs.readFileSync(connFile, "utf-8"));
            curl=conndata.httpconntion+rURL
            upam=""
            if(req.query!={}){for(key in req.query){upam+=key+"="+encodeURI(req.query[key])+"&"}}
            if(upam,upam!="")curl+="?"+upam
            
            resData=httpClient(curl,conndata.header);
        }
        else resData={code:500,msg:"文件不存在"}
    }
    console.log('get',path)
    console.log("query",JSON.stringify(req.query))
    console.log("body",JSON.stringify(req.body))
    console.log("params",JSON.stringify(req.params))
    console.log("result",JSON.stringify(resData,null,4))
    if(resData)res.send(resData)
});
router.post('(*)', (req, res)=> {
    let path=(webroot+req.params[0])
    let ext=paths.extname(path)
    let stats=err=resData=filedata=null;

    if (typeof (req.body.data) == "string") filedata=req.body.data;
    else if(isJson(req.body.data)) filedata=JSON.stringify(req.body.data,null, 4);
    if(fs.existsSync(path)){
        stats=fs.statSync(path)
        if(stats.isFile()){
            fs.writeFileSync(path,filedata); 
            resData={code:200,method:"post",file:"/webfs"+req.params[0]}        
        }
    }
    else{
        if(req.body.type=="file"){
            
            if(exts.indexOf(ext)==-1){
                fs.writeFileSync(path,filedata);
                resData={code:200,method:"post",file:"/webfs"+req.params[0]};
            }else if(ext==".ulnk" && paths.basename(path)!="conn.ulnk"){
                //如果是ulnk文件，查找是否有conn.ulnk，如果没有，则寻找上级
                if(!(fs.existsSync(paths.dirname(path)+"/conn.ulnk"))){ulinkPath.forEach(function(item){if(paths.dirname(path).indexOf(item)!=-1)connFile=item+"/conn.ulnk";})}
                else connFile=paths.dirname(path)+"/conn.ulnk";
                resData={code:200,conn:JSON.parse(fs.readFileSync(connFile, "utf-8")),file:JSON.parse(fs.readFileSync(path, "utf-8"))}
            }
        }else{resData={code:500,msg:err}}
    }
    if(resData)res.send(resData)
});
//路由写完了，现在可以把该数据库返回到操作层了
module.exports=router;