(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-22d96099"],{"2e7e":function(e,t,a){"use strict";a.r(t);var s=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{attrs:{id:"login_frame"}},[a("form",{attrs:{method:"post",name:"register"}},[a("p",[a("label",[e._v("用户名: ")]),a("input",{directives:[{name:"model",rawName:"v-model",value:e.username,expression:"username"}],staticClass:"text_field",domProps:{value:e.username},on:{input:function(t){t.target.composing||(e.username=t.target.value)}}})]),a("p",[a("label",[e._v("    邮箱: ")]),a("input",{directives:[{name:"model",rawName:"v-model",value:e.email,expression:"email"}],staticClass:"text_field",domProps:{value:e.email},on:{input:function(t){t.target.composing||(e.email=t.target.value)}}})]),a("p",[a("label",[e._v("    密码: ")]),a("input",{directives:[{name:"model",rawName:"v-model",value:e.password,expression:"password"}],staticClass:"text_field",attrs:{type:"password"},domProps:{value:e.password},on:{input:function(t){t.target.composing||(e.password=t.target.value)}}})]),a("div",{staticClass:"login_control"},[a("button",{staticClass:"login_button",on:{click:function(t){return t.stopPropagation(),t.preventDefault(),e.register(t)}}},[e._v("注册")]),a("button",{staticClass:"login_button",on:{click:function(t){return t.stopPropagation(),t.preventDefault(),e.login(t)}}},[e._v("已有账号去登录")])])])])},n=[],o={name:"Register",data:function(){return{username:"",email:"",password:""}},methods:{register:i,login:r}};function i(){var e=this,t="http://localhost:8000/v1/register";this.$http.post(t,{username:this.username,email:this.email,password:this.password}).then(function(t){0==t.data.code?(alert("注册成功"),e.$router.push({path:"/login"})):alert("code:"+t.data.code+"  message:"+t.data.message+t.data.data)})}function r(){this.$router.push("/login")}var l=o,u=(a("b6f3"),a("a6c2")),p=Object(u["a"])(l,s,n,!1,null,"106f86f8",null);p.options.__file="Register.vue";t["default"]=p.exports},"620d":function(e,t,a){},b6f3:function(e,t,a){"use strict";var s=a("620d"),n=a.n(s);n.a}}]);
//# sourceMappingURL=chunk-22d96099.9ea12fa2.js.map