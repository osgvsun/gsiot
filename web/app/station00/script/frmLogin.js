var frmLogin=new Form("frmLogin")
frmLogin.load=function(){
    App.frm=frmLogin;
    frmLogin.parent=new Element("panwork");
    // frmLogin.tmpl="".LoadURL(App.data.api.case).replace("<uvccamera>","".LoadURL(App.data.api.uvccamer).replace("<host>", App.data.cfg.ip)).replace("<host>",App.data.cfg.ip)
    // frmLogin.Show();
    // $ID("showpic").Error(frmLogin.OpenUsbCamera)
    App.wsc.event_receive=App.frm.Windows_Receive
}
frmLogin.Form_Receive=function(data){
    console.log(frmLogin.Name+" receive:"+JSON.stringify(data))
}