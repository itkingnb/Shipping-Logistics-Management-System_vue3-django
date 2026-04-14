<template>
  <h2>button disabled的值：  {{msg}}</h2>
  <h2>更改disabled 的值</h2>
  <input type="text" v-model="btn">
  <button @click="okfun">确定 </button>
  <hr>
  <button :disabled="btn" @click="fun">问好</button>
</template>
<script setup>
import {ref} from 'vue'
 let btn=ref(false)
 let msg=ref(btn)
 
 function fun(){
  console.log(`${msg.value}`)
  alert("您好！vue3")
 }
 function okfun(){
  btn.value=!btn.value
 }
</script>

<style scoped>

</style>
