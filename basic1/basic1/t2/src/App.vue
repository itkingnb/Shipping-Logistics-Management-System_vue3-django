<template>
<div class="txt1">
  <h2> {{stu.sid}} </h2>
  <h2> {{stu.name}} </h2>
  <h2> {{stu.dept}} </h2>
</div>
<button @click="upd">该专业为航海技术</button>
  
</template>

<script setup>
 import {reactive} from 'vue'
 let stu=reactive({
   sid:1001,
   name:"金同学",
   dept:"计算机"
 })
 function upd(){
   stu.dept="航海技术"
 }

</script>

<style scoped>
  .txt1{
    padding: 10px;
    background-color: gray;
    border-radius: 20px;
  }
</style>
