var express = require('express');
// var confDb = require('../db');
var rp = require('request-promise');
var control = function (app) {
  var _basepath = ''
  //映射app的get和post方法
  this.get = function (path, fn) {app.get(_basepath + path, fn)}
  this.post = function (path, fn) {app.post(_basepath + path, fn)}
  //按照时间生成唯一的GUID
  this.newGuid = function () {
    var guid = ''
    for (var i = 1; i <= 32; i++) {
      var n = Math.floor(Math.random() * 16.0).toString(16)
      guid += n
      if ((i == 8) || (i == 12) || (i == 16) || (i == 20))
        guid += '-'
    }
    return guid
  }
  //检查变量的值是否是数字
  this.checknumber = function (value) {
    var re = /^[0-9]+.?[0-9]*$/; // 判断字符串是否为数字 //判断正整数 /^[1-9]+[0-9]*]*$/ 
    var nubmer = value

    if (!re.test(nubmer))  return false
    else return true
  }
  this.basepath = function (value) {
    if (value != null)_basepath = value
    else return _basepath
  }
  // 文件服务器解密
   this.miniToken = function (request,result) {
        // 文件服务器解密
        for(var i=0;i<result.length;i++){
            // (site_image || url) && 包含39.108.175.164:8888
            var site_image = result[i].site_image
            var url = result[i].url
            url = url || site_image
            if(url&&url.indexOf('39.108.175.164')!=-1){
                // 截取除"http://"外
                url = url.substring(7)
                // 截取除"39.108.175.164:8888/"外
                url = url.substring(url.indexOf("/")+1)
                // 获取第一个"/"出现的位置
                var pos = url.indexOf("/")
                // 判断格式
                if(pos>0&&pos!=url.length-1){
                    // 截取group1
                    var group = url.substring(0,pos)
                    // 截取group1/之后
                    var murl = url.substring(pos+1)
                    // 秘钥
                    var secret = 'gs123GSgengshang'
                    // 时间
                    var ts = Math.floor(new Date().getTime()/1000)
                    // 调用教学平台接口
                    var jxurl = "http://localhost:8760/gvsunTms/system/miniToken?url="+murl+'&ts='+ts+"&key="+secret
                    var token = result[i].url
                    request(jxurl, function (error, response, body) {
                        if (!error && response.statusCode == 200) {
                            console.log('返回防盗链token值:'+body)
                            console.log('调用教学平台接口成功:'+jxurl)
                            token += '?token='+body+'&ts='+ts
                            console.log(token)
                        }else{
                            console.log('调用教学平台接口失败:'+jxurl)
                        }
                    })
                    // 把token封进返回数组中
                    // result[i].token = '?token='+token+'&ts='+ts
                }
            }
        }
    }
  // 统一接口调用入口
    this.gsteachAPI = function(uri,qs,token,school,fn){
        var options = {
            uri: uri,
            qs: qs,
            headers: {
                // 'Authorization':token,
                'User-Agent': 'Request-Promise',
                'cookie':'datasource.cookie=' + school,
                'x-datasource':''+school
            },
            method:'POST',
            json: true
        };
        var result = [];
        rp(options)
            .then(function (repos) {
                // API call success...
                result = result.concat(repos)
            })
            .catch(function (req,err) {
                // API call failed...
                console.log('fail')
                result = result.concat('api failed')
            })
            .finally(function () {
                // 接口调用无论成功与否,最后的返回
                console.log(options)
                console.log(result)
                fn(result)
            });
    }

    this.cmsAPI = function(uri,qs,token,fn){
        var options = {
            uri: uri,
            qs: qs,
            headers: {
                // 'Authorization':token,
                'User-Agent': 'Request-Promise',
            },
            method:'GET',
            json: true
        };
        var result = [];
        rp(options)
            .then(function (repos) {
                // API call success...
                result = result.concat(repos)
            })
            .catch(function (req,err) {
                // API call failed...
                console.log('fail')
                result = result.concat('api failed')
            })
            .finally(function () {
                // 接口调用无论成功与否,最后的返回
                console.log(options)
                console.log(result)
                fn(result)
            });
    }

    this.configcenterAPI = function(uri,qs,token,school,fn){
        var options = {
            uri: uri,
            body: qs,
            headers: {
                'User-Agent': 'Request-Promise',
                'cookie':'datasource.cookie=' + school,
                'x-datasource':''+school
             },
            contentType: 'application/json;charset=utf-8',
            method:'POST',
            json: true
        };
        var result = [];
        rp(options)
            .then(function (repos) {
                // API call success...
                result = result.concat(repos)
            })
            .catch(function (req,err) {
                // API call failed...
                console.log('fail')
                result = result.concat('api failed')
            })
            .finally(function () {
                // 接口调用无论成功与否,最后的返回
                console.log(options)
                console.log(result)
                fn(result)
            });
    }

    this.usercenterApi=function (uri,qs,school,fn) {
    var options = {
        uri: uri,
        qs: qs,
        headers: {
            // 'Authorization':token,
            'User-Agent': 'Request-Promise',
            'cookie':'datasource.cookie=' + school,
            'x-datasource':''+school
        },
        method:'GET',
        json: true
    };
    var result = [];
    rp(options)
        .then(function (repos) {
            // API call success...
            result = result.concat(repos)
        })
        .catch(function (req,err) {
            // API call failed...
            console.log('fail')
            result = result.concat('api failed')
        })
        .finally(function () {
            // 接口调用无论成功与否,最后的返回
            console.log(options)
            console.log(result)
            fn(result)
        });
}

    // oauth2 用户登录关联接口
    this.oauth2Login = function(uri,qs,fn){
        var options = {
            uri: uri,
            qs: qs,
            headers: {
                // 'Authorization':token,
                'User-Agent': 'Request-Promise',
                // 'cookie':'datasource.cookie=' + school
            },
            method:'GET',
            json: true
        };
        var result = [];
        rp(options)
            .then(function (repos) {
                // API call success...
                result = result.concat(repos)
            })
            .catch(function (req,err) {
                // API call failed...
                console.log('fail')
                result = result.concat('api failed')
            })
            .finally(function () {
                // 接口调用无论成功与否,最后的返回
                console.log(options)
                console.log(result)
                fn(result)
            });
    }


    // 资源容器
    this.resourceContainer = function(uri,qs,token,school,fn){
        var options = {
            uri: uri,
            qs: qs,
            headers: {
                // 'Authorization':token,
                'User-Agent': 'Request-Promise',
                'cookie':'datasource.cookie=' + school,
                'x-datasource':''+school
            },
            method:'GET',
            json: true
        };
        var result = [];
        rp(options)
            .then(function (repos) {
                // API call success...
                result = result.concat(repos)
            })
            .catch(function (req,err) {
                // API call failed...
                console.log('fail')
                result = result.concat('api failed')
            })
            .finally(function () {
                // 接口调用无论成功与否,最后的返回
                console.log(options)
                console.log(result)
                fn(result)
            });
    }


    // 文件服务器
    this.resourceUpload = function(uri,qs,body,token,school,fn){
        var options = {
            uri: uri,
            qs: qs,
            body:body,
            headers: {
                // 'Authorization':token,
                'User-Agent': 'Request-Promise',
                'cookie':'datasource.cookie=' + school,
                'x-datasource':''+school
            },
            method:'GET',
            json: true
        };
        var result = [];
        rp(options)
            .then(function (repos) {
                // API call success...
                result = result.concat(repos)
            })
            .catch(function (req,err) {
                // API call failed...
                console.log('fail')
                result = result.concat('api failed')
            })
            .finally(function () {
                // 接口调用无论成功与否,最后的返回
                console.log(options)
                console.log(result)
                fn(result)
            });
    }
}

module.exports = control
