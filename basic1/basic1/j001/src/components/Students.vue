<template>
   <h1>{{stu.sid++}} </h1>
  <h1>{{stu.name}} </h1>
  <button @click="update1">aaa</button>
</template>

<script setup>
import {ref,reactive} from 'vue'
let stu=reactive({
    sid:1001,
    name:"jss"
})
function update1(){
    stu.name="smu"
}
 
</script>

<style>

</style>