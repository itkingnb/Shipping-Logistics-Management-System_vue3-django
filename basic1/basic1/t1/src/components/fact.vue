<template>
  <input type="text" v-model="n">
  <h2> n 的值的为： {{n}}</h2>
  <button @click="fun(n)">求阶乘</button>
  <h2> n 的阶乘为： {{s}}</h2>
</template>

<script setup>
import {ref} from 'vue'
 let s=ref(1)
 let n=ref(1)
 function fun(n){
    let i=1
    s.value=1
    for(i=1;i<=n;i=i+1){
        s.value=s.value*i
    }
 }


</script>
<style scoped>

</style>