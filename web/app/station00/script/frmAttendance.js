App.frmAttendance=new Form("frmAttendance");frmAttendance=App.frmAttendance;
App.frmAttendance.load=function(){
    App.frm=frmAttendance;
    frmAttendance.parent=new Element("panwork");
    frmAttendance.tmpl="".LoadURL(App.data.tmpl.frmAttendance);
    App.wsc.event_receive=App.frmAttendance.Windows_Receive;
}
App.frmAttendance.Form_Receive=function(data){
    console.log(frmAttendance.Name+" receive:"+JSON.stringify(data))
}