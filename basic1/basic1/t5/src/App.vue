<template>
  <img :src="path">
  <input type="text" v-model="path">
  <select @change="handleChange($event)">
    <option v-for="(item,index) in arr" :key="index" >{{item}}</option>
  </select>
</template>

<script setup>
import {ref,reactive}  from 'vue'
let path= ref("one.jpg")
let arr=reactive(["one.jpg","two.jpg","three.jpg"])
function handleChange(event){
  //path.value=arr[2]
    this.selected = event.target.value;
    console.log('Selected value:', this.selected)
    path.value=this.selected 
}
</script>

<style scoped>

</style>
