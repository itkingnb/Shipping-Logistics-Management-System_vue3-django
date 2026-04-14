<template>
 <jin/>
  <div class="txt1">  
    <students/>
   <button @click="f1">测试</button>
  </div>
</template>

<script setup>
import {ref,reactive} from 'vue'
import jin from './components/jin.vue'
import Students from './components/Students.vue'

let x=ref(0)
let y=ref(0)
let s=ref(0)
function f1(event){
  alert(`hello ${x.value}`)
  if (event) {
    alert(event.target.tagName)
  }
}
function add1(){
  s.value=x.value*1.0+y.value*1.0  //int()
}
</script>

<style scoped>
.txt1{
  font-size: 36px;
  background-color: cadetblue;
  padding: 10px;
  border-radius: 20px;
}
input{
  font-size: 36px; 
}
</style>
