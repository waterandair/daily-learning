(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-d239c93e"],{"518d":function(t,e,n){"use strict";var o=n("a96c"),a=n.n(o);a.a},"9c23":function(t,e,n){"use strict";n.r(e);var o=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"create-post"},[n("form",{attrs:{method:"post",name:"create"}},[n("textarea",{directives:[{name:"model",rawName:"v-model",value:t.content,expression:"content"}],domProps:{value:t.content},on:{input:function(e){e.target.composing||(t.content=e.target.value)}}}),n("button",{on:{click:function(e){return e.stopPropagation(),e.preventDefault(),t.create_post(e)}}},[t._v("提交"+t._s(t.content))])])])},a=[],c=(n("dd5c"),n("9cf8"),n("a66e"),{name:"PostCreate",data:function(){return{content:"new post"}},methods:{create_post:function(){var t=this;console.log(this.content);var e="http://localhost:8000/v1/post/create";this.$http.post(e,{content:this.content}).then(function(e){0==e.data.code&&(alert("提交成功"),t.$router.push({path:"/"}))})}}}),s=c,r=(n("518d"),n("a6c2")),i=Object(r["a"])(s,o,a,!1,null,"1d5ed8d4",null);i.options.__file="PostCreate.vue";e["default"]=i.exports},a96c:function(t,e,n){}}]);
//# sourceMappingURL=chunk-d239c93e.140258e5.js.map