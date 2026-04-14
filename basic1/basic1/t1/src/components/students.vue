<template>
<h2>{{sid}}</h2>
<h2>{{name}}</h2> 
<h2>{{mob}}</h2>
<hr>
<input type="text" v-model="mob">
<button @click="updatemob">修改手机号</button>
<button @click="show">显示手机号</button>
</template>

<script setup>
 import {ref} from 'vue'
 let sid=ref(1001)
 let name=ref("金同学")
 let mob=ref(18918888888)
 function updatemob(){
    mob.value=18918855581
 }
 function show(){
    alert(mob.value)
 }
</script>

<style scoped>

</style>
