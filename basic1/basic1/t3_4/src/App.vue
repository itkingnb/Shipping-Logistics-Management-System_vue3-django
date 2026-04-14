<template>
<p class="txt1">
  {{msg}}
  <br>
  简单的Javascript 表达式：  {{count+10}}
  <br>
  ？ ： 运算符：  {{yn?"yes":"no"}}
  <br>
  字符串函数的应用： {{st.split('').reverse().join('')}}
</p>
<p>{{htl}}</p>
<p v-html="htl"></p>
</template>
<script setup>
import {ref} from 'vue'
 let msg=ref("Hello 金！")
 let count=0
 let yn=true
 let st="前端开发"
 let htl="<a href='http://www.shanghai.gov.cn' target='_blank'>上海</a>"
console.log(`${msg.value}`)
</script>

<style scoped>
.txt1{
  padding:0px ;
  background-color: darkgrey;
  font-size:24px; 
  top:1px;
  text-align: left;
}
/* p{
  vertical-align: top;
} */
</style>
